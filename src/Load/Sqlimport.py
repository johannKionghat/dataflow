import os
import re
import yaml
import pymysql
import sqlite3
import psycopg2  # Redshift = PostgreSQL compatible
import boto3

def load_config(path='config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def read_sql_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def create_jobs_table(cursor, db_type):
    drop_sql = "DROP TABLE IF EXISTS jobs;"
    cursor.execute(drop_sql)

    create_sql = """
    CREATE TABLE jobs (
        job_title TEXT,
        company TEXT,
        location TEXT,
        description TEXT
    );
    """
    if db_type == 'mysql':
        create_sql = create_sql.replace("TEXT", "VARCHAR(1000)")
    elif db_type == 'redshift':
        create_sql = create_sql.replace("TEXT", "VARCHAR(65535)")
    
    cursor.execute(create_sql)


def execute_sql(cursor, sql_text):
    statements = re.split(r';\s*\n', sql_text.strip())
    for stmt in statements:
        if stmt.strip():
            cursor.execute(stmt)

def import_to_mysql(cfg, sql_text):
    conn = pymysql.connect(**cfg, charset='utf8mb4')
    cursor = conn.cursor()
    create_jobs_table(cursor, 'mysql')
    execute_sql(cursor, sql_text)
    conn.commit()
    conn.close()

def import_to_sqlite(cfg, sql_text):
    conn = sqlite3.connect(cfg['filepath'])
    cursor = conn.cursor()
    create_jobs_table(cursor, 'sqlite')
    execute_sql(cursor, sql_text)
    conn.commit()
    conn.close()

def import_to_redshift(cfg, sql_text):
    conn = psycopg2.connect(
        host=cfg['host'],
        user=cfg['user'],
        password=cfg['password'],
        dbname=cfg['database'],
        port=cfg.get('port', 5439)
    )
    cursor = conn.cursor()
    create_jobs_table(cursor, 'redshift')
    execute_sql(cursor, sql_text)
    conn.commit()
    conn.close()

def main():
    config = load_config()
    db_type = config['database']['type']
    db_cfg = config['database'][db_type]
    sql_path = config['sql_path']

    if not os.path.exists(sql_path):
        print(f"❌ Fichier SQL introuvable : {sql_path}")
        return

    sql_text = read_sql_file(sql_path)

    print(f"ℹ️  Import vers {db_type.upper()}...")

    if db_type == 'mysql':
        import_to_mysql(db_cfg, sql_text)
    elif db_type == 'sqlite':
        import_to_sqlite(db_cfg, sql_text)
    elif db_type == 'redshift':
        import_to_redshift(db_cfg, sql_text)
    else:
        print(f"❌ Type de base de données non supporté : {db_type}")
        return

    print("✅ Importation terminée avec succès.")

if __name__ == '__main__':
    main()
