import os
import json
import pandas as pd

def scraping_transform():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # dossier de scraping.py
    file_path = os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'raw', 'json', 'scraping.json')
    file_path = os.path.normpath(file_path)  # normaliser le chemin

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame([data])
    print('Nettoyage des données')
    df_clean = df.copy()
    print('Sélection des colonnes')
    df_clean.rename(columns={"Job_Title": "Job_title"}, inplace=True)
    df_clean = df_clean.drop_duplicates()
    
    output_path = os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'processed', 'df_clean_welcometothejungle.csv')
    output_path = os.path.normpath(output_path)

    df_clean.to_csv(output_path, index=False)
    print(f"✅ Données transformées et sauvegardées dans : {output_path}")
    print(df_clean.head())

if __name__ == "__main__":
    scraping_transform()
