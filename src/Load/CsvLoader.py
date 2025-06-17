import os
import pandas as pd
from datetime import datetime

def save_df_to_csv(df: pd.DataFrame, filename: str = None, output_dir: str = 'data/dataLake/raw/csv'):
    """
    Sauvegarde un DataFrame en fichier CSV.

    Args:
        df (pd.DataFrame): Le DataFrame à sauvegarder
        filename (str, optional): Nom du fichier sans extension. Si None, génère un nom auto.
        output_dir (str): Répertoire de sauvegarde. Défaut = 'data/csv'

    Returns:
        str: Chemin du fichier CSV créé
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not filename:
        filename = f"dataframe"

    file_path = os.path.join(output_dir, f"{filename}.csv")
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

    print(f"✅ CSV saved at: {file_path}")
    return file_path
