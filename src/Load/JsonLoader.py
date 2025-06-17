import json
import os
from datetime import datetime

def jsonLoader(data, source_name):
    os.makedirs(f"data/dataLake/raw/json/", exist_ok=True)
    path = f"data/dataLake/raw/json/{source_name}.json"
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Données sauvegardées dans : {path}")
