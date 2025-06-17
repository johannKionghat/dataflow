import pandas as pd

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = pd.read_json(file)
    return data
