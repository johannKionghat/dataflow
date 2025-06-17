import os
import pandas as pd

def csv_indeed_transform():
    # Définition des chemins
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
    input_path = os.path.normpath(os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'raw', 'csv', 'df_all_indeed.csv'))
    output_path = os.path.normpath(os.path.join(base_dir, '..', '..', 'data', 'dataLake', 'processed', 'df_clean_indeed.csv'))

    # Chargement du fichier
    df = pd.read_csv(input_path)
    print("🔍 Lecture du fichier brut terminée")

    # Sélection des colonnes
    columns_to_keep = ["Jobs", "Companies", "Locations", "Summary"]
    missing = set(columns_to_keep) - set(df.columns)
    if missing:
        raise ValueError(f"❌ Colonnes manquantes dans le fichier Indeed : {missing}")

    df_clean = df[columns_to_keep].copy()

    # Renommage des colonnes pour correspondre au format standardisé
    df_clean.rename(columns={
        "Jobs": "job_title",
        "Companies": "company",
        "Locations": "location",
        "Summary": "description"
    }, inplace=True)

    # Nettoyage des valeurs texte : trim + lower
    df_clean = df_clean.applymap(lambda x: str(x).strip().lower() if pd.notnull(x) else '')

    # Suppression des doublons
    initial_len = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    final_len = len(df_clean)
    print(f"🧹 {initial_len - final_len} doublon(s) supprimé(s)")

    # (Optionnel) Suppression des lignes vides
    df_clean = df_clean[~(df_clean == '').all(axis=1)]

    # Sauvegarde du résultat
    df_clean.to_csv(output_path, index=False)
    print(f"✅ Données transformées et sauvegardées dans : {output_path}")
    print(df_clean.info())
    print(df_clean.head())

if __name__ == "__main__":
    csv_indeed_transform()
