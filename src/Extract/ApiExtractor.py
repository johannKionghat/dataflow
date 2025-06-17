# etl/extractors/ApiExtractor.py

import requests

class ApiExtractor:
    """
    Classe responsable de l'extraction de données depuis une API.
    """

    def __init__(self, url, headers=None, params=None, method='GET'):
        """
        Initialise l'extracteur d'API.
        :param url: URL de l'API
        :param headers: Dictionnaire des en-têtes HTTP (ex : token)
        :param params: Paramètres de la requête (query string)
        :param method: Méthode HTTP (GET, POST...)
        """
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.method = method.upper()

    
    def fetch(self):
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])

        except requests.exceptions.RequestException as e:
            error_msg = f"""
            Erreur API:
            - URL: {self.url}
            - Headers: {self.headers}
            - Params: {self.params}
            - Message: {str(e)}
            """
            raise RuntimeError(error_msg)
