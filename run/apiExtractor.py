import yaml
from src.Extract.ApiExtractor import ApiExtractor

def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    config = load_config("config.yaml")
    extractor = ApiExtractor(url=config['api']['url'], headers=config['api']['headers'], params=config['api']['params'], method=config['api']['method'])
    results = extractor.fetch()
    print(f"{len(results)} lignes récupérées")
    if results:
        print("Exemple :", results[0])
