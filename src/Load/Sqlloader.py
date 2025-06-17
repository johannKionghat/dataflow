import os
import pandas as pd

def df_to_sql_file(df, table_name, output_dir='data/dataWarehouse/'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, f"{table_name}.sql")

    # Création de la requête CREATE TABLE si elle n'existe pas
    create_table = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    job_title TEXT,
    company TEXT,
    location TEXT,
    description TEXT
);
"""

    # Écriture du fichier
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(create_table)
        for _, row in df.iterrows():
            values = ', '.join(
                [f"'{str(x).replace("'", "''")}'" if pd.notnull(x) else 'NULL' for x in row]
            )
            columns = ', '.join(df.columns)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n"
            f.write(sql)

    print(f"✅ SQL file saved: {file_path}")
    return file_path
