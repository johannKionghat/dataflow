# run/scrapingExtractor.py

import yaml
from src.Extract.ScrapingExtractor import ScrapingExtractor

def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    config = load_config("config.yaml")
    url = config['scraping']['url']

    extractor = ScrapingExtractor(url=url)
    page_text = extractor.fetch()

    print("=== Contenu de la page ===")
    print(page_text[:1000])  # Affiche seulement les 1000 premiers caractères pour éviter l’encombrement
