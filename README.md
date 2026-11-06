# Projet Fil Rouge

## Description
Sur base de l'API Open Meteo, ce projet consiste à restistuer les infos récupérées par requêtes HTTP sur une interface lisible

## Installation

Exécutez dans un terminal :

```bash
python3 -m venv .venv
pip install -r requirements.txt
```

Pour lancer le projet :     
***ATTENTION !!! Lancez les commandes sur des terminals séparés pour ne pas interrompre Streamlit ou FastAPI***

```bash
streamlit run app/front/app.py
uvicorn app.back.back:app --reload
```

***NOTE !!*** : Si la base de données n'est pas encore créée dans le repertoire data, vous pouvez exécuter cette commande :

```bash
python3 app/back/db_functions/db.py
```

## Architecture du projet
```
├── app
│   ├── back                # Répertoire de la partie Back-End où se trouve 
│   │   ├── back.py         # Interface FastAPI
│   │   ├── data            # Dossier où se trouve la base de données
│   │   └── db_functions
│   │       └── db.py       # Gestionnaire de la base de données
│   └── front
│       ├── app.py          # Point d'entrée principal de l'interface Front-End avec Streamlit
│       └── pages
│           ├── 1_data.py   # Page d'affichage des données
│           └── 2_add.py    # Page d'ajout d'une nouvelle vide
├── README.md               # Documentation du projet
├── requirements.txt        # Modules à installer avec pip
├── .env.example            # Variables d'environnement pour les liens vers l'API et la base de données
└── schemas
    ├── city_data.py        # Modèle Pydantic pour les données d'une ville
    └── wheather_response.py # Modèle Pydantic pour les relevés météo d'une ville
```

## Technologies utilisés

- FastAPI - Swagger : Technologie de Back-End utilisée pour créer une interface d'API, utilisée la communication avec la base de données via des requêtes HTTP. Swagger se charge quand à lui de documenter automatiquement l'API.

La documentation de l'API de ce projet se trouve sur :  http://127.0.0.1:8000/docs

***Veillez à lancer le server FastAPI avant de pouvoir y accéder***


- Streamlit : Technologie utilisé pour la réalisation de l'interface Front-End, connecté avec FastAPI.

- Pydantic : Utilisé pour créer des modèles de validation de données, avant toute insertion dans la base de données.

- Pandas : Utilisé pour la création de Dataframes avec les données JSON des requêtes FastAPI, affichées ensuite avec Streamlit.

## APIs utilisés :

- Open Meteo : API principale pour récupèrer les relevés météo d'un ville grâce aux requêtes GET. Elle permet de renvoyer des informations comme la vitesse du vent, la température, etc...

https://open-meteo.com/


- Nominatim : API utilisant OpenStreetMap pour récupérer les coordonnées précise d'une ville
