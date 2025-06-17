import yaml
from src.Extract.CsvExtractor import CsvExtractor

def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    config = load_config()
    extractor = CsvExtractor(csv_path=config['csv']['path'])
    results = extractor.fetch()
    print(f"{len(results)} lignes récupérées")
    if results:
        print("Exemple :", results[0])
