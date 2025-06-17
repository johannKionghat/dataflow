import os
import json
import pandas as pd

def api_transform():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # dossier de scraping.py
    file_path = os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'raw', 'json', 'api.json')
    file_path = os.path.normpath(file_path)  # normaliser le chemin

    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        data = json.load(f)

    # Si data est une liste de jobs
    if isinstance(data, list):
        df = pd.json_normalize(data)
    # Si c'est un dict avec une clé contenant la liste
    elif isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, list):
                df = pd.json_normalize(val)
                break
        else:
            df = pd.json_normalize(data)
    
    cols_dict = [col for col in df.columns if df[col].apply(contains_dict).any()]
    for col in cols_dict:
        df[col] = df[col].apply(convert_dicts)
    cols_list = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).any()]
    for col in cols_list:
        df[col] = df[col].apply(lambda x: tuple(x) if isinstance(x, list) else x)

    # Nettoyage des données
    print('Nettoyage des données')
    df_clean = df.copy()
    # Colonnes à sélectionner (les noms d'origine)
    print('Sélection des colonnes')
    columns_to_keep = ["job_title", "employer_name", "job_location", "job_description"]
    # Sélection du sous-DataFrame avec ces colonnes
    df_clean = df_clean[columns_to_keep].copy()
    # Renommage des colonnes
    print('Renommage des colonnes')
    df_clean.rename(columns={
        "job_title": "Job_title",
        "employer_name": "Company",
        "job_location": "Location",
        "job_description": "Description"
    }, inplace=True)
    df_clean = df_clean.drop_duplicates()
    output_path = os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'processed', 'df_clean_api.csv')
    output_path = os.path.normpath(output_path)

    df_clean.to_csv(output_path, index=False)
    print(f"✅ Données transformées et sauvegardées dans : {output_path}")
    print(df_clean.head())

def contains_dict(x):
    if isinstance(x, dict):
        return True
    if isinstance(x, (list, tuple)):
        return any(isinstance(i, dict) for i in x)
    return False

def convert_dicts(x):
    if isinstance(x, dict):
        return str(x)
    elif isinstance(x, (list, tuple)):
        return tuple(str(i) if isinstance(i, dict) else i for i in x)
    else:
        return x

if __name__ == "__main__":
    api_transform()
