import os
import pandas as pd

def concat_all_data():
    # Chemin de base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'processed')

    # Chargement des fichiers CSV
    indeed = pd.read_csv(os.path.join(file_path, 'df_clean_indeed.csv'))
    linkedin = pd.read_csv(os.path.join(file_path, 'df_clean_linkedin.csv'))
    api = pd.read_csv(os.path.join(file_path, 'df_clean_api.csv'))
    scraping = pd.read_csv(os.path.join(file_path, 'df_clean_welcometothejungle.csv'))

    # Harmonisation des noms de colonnes
    for df in [indeed, linkedin, api, scraping]:
        df.columns = df.columns.str.lower().str.strip()

    # Colonnes attendues (modifie si nécessaire)
    expected_columns = ['job_title', 'company', 'location', 'description']
    for name, df in zip(['Indeed', 'LinkedIn', 'API', 'Scraping'], [indeed, linkedin, api, scraping]):
        missing_cols = set(expected_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"❌ Colonnes manquantes dans {name} : {missing_cols}")
        df = df[expected_columns]

    # Concaténation
    print("🛠️  Concaténation des données...")
    df_all = pd.concat([indeed[expected_columns], linkedin[expected_columns], api[expected_columns], scraping[expected_columns]], ignore_index=True)

    # Nettoyage des chaînes de caractères : trim, lower
    df_all = df_all.applymap(lambda x: str(x).strip().lower() if pd.notnull(x) else '')

    # Suppression des doublons
    initial_len = len(df_all)
    df_all.drop_duplicates(inplace=True)
    final_len = len(df_all)
    print(f"✅ {initial_len - final_len} doublon(s) supprimé(s).")

    # (Optionnel) Suppression des lignes vides (si toutes les colonnes sont vides)
    df_all = df_all[~(df_all == '').all(axis=1)]

    # Sauvegarde
    output_path = os.path.join(file_path, 'df_clean_all.csv')
    df_all.to_csv(output_path, index=False)

    print(f"✅ Données concaténées et sauvegardées dans : {output_path}")
    print(df_all.info())
    print(df_all.head())

    return df_all

if __name__ == "__main__":
    concat_all_data()
