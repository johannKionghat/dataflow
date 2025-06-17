import yaml
import pandas as pd
import subprocess

from src.Extract.ApiExtractor import ApiExtractor
from src.Extract.ScrapingExtractor import ScrapingExtractor
from src.Load.JsonLoader import jsonLoader
from src.Extract.SqlExtractor import get_dataframe_from_db
from src.Load.Sqlloader import df_to_sql_file
from src.Transformers.api import api_transform
from src.Transformers.indeed import csv_indeed_transform
from src.Transformers.linkedin import csv_linkedin_transform
from src.Transformers.scraping import scraping_transform
from src.Transformers.all_data import concat_all_data
from src.Load.Sqlimport import main as sql_import

def load_config(config_path):
    """Charge la configuration depuis un fichier YAML."""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier de configuration {config_path} est introuvable.")
    except yaml.YAMLError as e:
        raise ValueError(f"Erreur de syntaxe dans le fichier de configuration: {e}")

def run_api_extractor(config):
    # Extraction des données via API
    extractor = ApiExtractor(
        url=config['api']['url'],
        headers=config['api']['headers'],
        params=config['api']['params'],
        method=config['api']['method']
    )
    results = extractor.fetch()
    print(f"[API] {len(results)} éléments récupérés.")
    if results:
        print("[API] Premier élément :", results[0])
    # Sauvegarde des données
    jsonLoader(results, "api")

def run_scraping_extractor(config):
    # Extraction des données via scraping
    extractor = ScrapingExtractor(
        url=config['scraping']['url'],
        mistral_api_key=config['mistral']['api_key']
    )
    results = extractor.fetch()
    print(f"[Scraping] {len(results)} éléments récupérés.")
    print("results :", results)
    # Sauvegarde des données
    jsonLoader(results, "scraping")
    

def run_sql_extractor():
    # Extraction des données
    query = "SELECT * FROM jobs;"
    df = get_dataframe_from_db(query, config_path='config.yaml')
    # Sauvegarde des données
    df_to_sql_file(df, "jobs")
    df.to_csv("data/visualisation/jobs.csv", index=False)
    print("Extraction des données dans le datawarehouse terminée")
    print(df.head())

def run_sql_loader():
    # Concaténation des données
    df = concat_all_data()
    # Sauvegarde des données
    df_to_sql_file(df, "jobs")

def run_transformer():
    # Transformation des données
    api_transform()
    csv_indeed_transform()
    csv_linkedin_transform()
    scraping_transform()
    
def run_sql_import():
    # Migration des données vers le datawarehouse
    sql_import()

def run_visualisation():
    subprocess.run(["streamlit", "run", "visualisation/app.py"])

def main():
    config = load_config("config.yaml")

    # Extraction des données API et scraping et sauvegarde dans le datalake
    run_api_extractor(config)
    run_scraping_extractor(config)

    # Transformation des données
    run_transformer()
    
    # Sauvegarde des données en sql
    run_sql_loader()

    # Migration des données vers le datawarehouse
    run_sql_import()

    # Recuperation des données dans le datawarehouse pour la visualisation
    print("Recuperation des données dans le datawarehouse pour la visualisation")
    run_sql_extractor()

    # Visualisation des données avec streamlit
    print("Visualisation des données")
    run_visualisation()

if __name__ == "__main__":
    main()
