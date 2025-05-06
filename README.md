# DataFlow - Un outil ETL modulaire en Python

## 📋 Table des matières
- [Introduction](#-introduction)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [Structure du projet](#-structure-du-projet)
- [Documentation technique](#-documentation-technique)
- [Contribution](#-contribution)
- [Licence](#-licence)

## 🌟 Introduction

DataFlow est un outil ETL (Extract-Transform-Load) modulaire développé en Python. Conçu pour être flexible et extensible, il permet de collecter, transformer et charger des données depuis et vers diverses sources.

## ✨ Fonctionnalités

### Extraction
- Lecture depuis des fichiers plats (CSV, TXT)
- Import depuis des fichiers structurés (JSON, XML, HTML)
- Connexion à des bases de données relationnelles
- Récupération de données via des API REST
- Support pour plusieurs sources simultanées

### Transformation
- Filtrage des données
- Nettoyage des valeurs manquantes ou aberrantes
- Calcul de nouvelles valeurs
- Normalisation des formats (dates, catégories, etc.)
- Agrégation et jointure de données

### Chargement
- Export vers des bases de données relationnelles
- Génération de fichiers (CSV, JSON, XML)
- Support pour plusieurs destinations simultanées

## 🚀 Installation

1. Cloner le dépôt :
   ```bash
   git clone [URL_DU_DEPOT]
   cd DataFlow
   ```

2. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Utilisation

### Configuration
Créez un fichier YAML de configuration pour définir votre pipeline ETL :

```yaml
pipeline:
  - extract:
      type: csv
      source: data/input/data.csv
  - transform:
      - filter:
          condition: "age > 18"
      - normalize:
          field: date
          format: "%Y-%m-%d"
  - load:
      type: postgresql
      table: users
      connection: postgresql://user:password@localhost/dbname
```

### Exécution

```bash
python -m dataflow run pipeline.yaml
```

## 🏗️ Architecture

L'application suit une architecture modulaire avec les composants principaux :

1. **Extract** : Gère la lecture des données depuis différentes sources
2. **Transform** : Applique les transformations aux données
3. **Load** : Gère l'écriture des données transformées
4. **Core** : Contient les fonctionnalités de base et les modèles de données

## 📁 Structure du projet

```
DataFlow/
├── data/                   # Données d'exemple
├── src/
│   ├── extract/           # Modules d'extraction
│   │   ├── csv.py
│   │   ├── api.py
│   │   └── scrapping.py
│   ├── transform/          # Modules de transformation
│   │   └── processor.py
│   ├── load/               # Modules de chargement
│   │   ├── csv.py
│   │   └── sql.py
│   └── core/               # Fonctionnalités de base
├── tests/                  # Tests unitaires
├── docs/                   # Documentation
├── requirements.txt        # Dépendances
└── README.md
```

## 📚 Documentation technique

Pour plus de détails sur l'API et les modules, consultez la [documentation technique](./docs/).

## 👥 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

Développé avec ❤️ par [Votre Équipe]
