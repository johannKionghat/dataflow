import yaml
import pandas as pd
import sqlite3
import boto3
import time
from sqlalchemy import create_engine
import psycopg2

def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_dataframe_from_db(query: str, config_path='config.yaml') -> pd.DataFrame:
    config = load_config(config_path)
    db_conf = config['database']
    db_type = db_conf['type']

    if db_type == 'mysql':
        db = db_conf['mysql']
        engine = create_engine(
            f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
        )
        return pd.read_sql(query, engine)

    elif db_type == 'sqlite':
        filepath = db_conf['sqlite']['filepath']
        conn = sqlite3.connect(filepath)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    elif db_type == 'redshift':
        db = db_conf['redshift']
        conn = psycopg2.connect(
            host=db['host'],
            port=db['port'],
            user=db['user'],
            password=db['password'],
            dbname=db['database']
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    elif db_type == 'athena':
        db = db_conf['athena']
        client = boto3.client('athena', region_name=db['region'])

        response = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': db['database']},
            ResultConfiguration={'OutputLocation': db['s3_output']}
        )

        query_execution_id = response['QueryExecutionId']

        while True:
            result = client.get_query_execution(QueryExecutionId=query_execution_id)
            state = result['QueryExecution']['Status']['State']
            if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(1)

        if state != 'SUCCEEDED':
            raise Exception(f"Athena query failed with state: {state}")

        output_path = f"{db['s3_output']}{query_execution_id}.csv"
        df = pd.read_csv(output_path)
        return df

    else:
        raise ValueError(f"Unsupported DB type: {db_type}")
