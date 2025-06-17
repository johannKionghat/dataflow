import requests
from bs4 import BeautifulSoup
import json
from mistralai import Mistral
class ScrapingExtractor:
    def __init__(self, url, mistral_api_key):
        self.url = url
        self.client = Mistral(api_key=mistral_api_key)

    def extract_text(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()
        full_text = soup.get_text(separator='\n')
        return '\n'.join(line.strip() for line in full_text.splitlines() if line.strip())

    def structure_with_mistral(self, text):
        prompt = f"""
        Voici une description brute d'une offre d'emploi :

        {text}

        Retourne-moi uniquement un objet JSON structuré avec les champs suivants :
        Job_Title, Company, Location, Description.

        - Toutes les valeurs doivent être explicites et réalistes.
        - Utilise les guillemets doubles (" ") pour les clés et les valeurs.
        - Ne retourne rien d'autre que le JSON brut. Aucun commentaire ou texte explicatif.

        Exemple :
        {{
        "Job_Title": "Développeur Python",
        "Company": "OpenAI",
        "Location": "Paris, France",
        "Description": "Vous travaillerez sur des modèles d'IA..."
        }}
"""
        model = "mistral-large-latest"
        chat_response = self.client.chat.complete(
            model = model,
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )
        json_string = chat_response.choices[0].message.content.strip()
        return json.loads(json_string)

    def fetch(self):
        text = self.extract_text()
        return self.structure_with_mistral(text)
