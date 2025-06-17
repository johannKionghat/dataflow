import os
import pandas as pd

def csv_linkedin_transform():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'raw', 'csv', 'df_all_linkedin.csv'))

    # Chargement du fichier
    df = pd.read_csv(file_path)
    print('🔍 Chargement du fichier CSV LinkedIn terminé.')

    # Vérification des colonnes attendues
    expected_columns = ["Job_Title", "Company", "Location", "Description"]
    missing_cols = set(expected_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"❌ Colonnes manquantes dans le fichier LinkedIn : {missing_cols}")

    print('✅ Sélection et copie des colonnes pertinentes...')
    df_clean = df[expected_columns].copy()

    print('✏️ Renommage des colonnes...')
    df_clean.rename(columns={
        "Job_Title": "job_title",
        "Company": "company",
        "Location": "location",
        "Description": "description"
    }, inplace=True)

    print('🧹 Nettoyage du texte (trim + lower)...')
    df_clean = df_clean.applymap(lambda x: str(x).strip().lower() if pd.notnull(x) else '')

    # Suppression des doublons
    initial_len = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    final_len = len(df_clean)
    print(f"✅ {initial_len - final_len} doublon(s) supprimé(s).")

    # Sauvegarde
    output_path = os.path.normpath(os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'processed', 'df_clean_linkedin.csv'))
    df_clean.to_csv(output_path, index=False)

    print(f"✅ Données transformées et sauvegardées dans : {output_path}")
    print(df_clean.head())

if __name__ == "__main__":
    csv_linkedin_transform()
