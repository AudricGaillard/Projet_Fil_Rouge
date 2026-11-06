# Fichier pour la gestion de l'API avec FastAPI

import os
import sys
import requests
from app.back.db_functions import db
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Ajout du dictionnaire parent au module de recherche Python, afin d'avoir les schèmas Pydantic
path_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if path_projet not in sys.path:
    sys.path.insert(0, path_projet)

from schemas import city_data, wheather_response


# Ce dictionnaire servira à l'insertion de données (voir ci-dessous)
headers = {
    "User-Agent": "test (mail@exemple.fr)"
}

# Route GET pour avoir les données de toutes les villes
@app.get('/villes')
async def names():
    """Renvoie toutes les villes et leurs infos"""
    try:
        # Appel du gestionnaire de base de données pour avoir les données
        response = db.get_weather_results()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur : {e}")


# Route POST pour insérer les données d'une nouvelle ville
@app.post('/ville/add', status_code=201)
async def add_city(city_name:str):
    """Ajoute une nouvelle ville et sa météo, ou met à jour les données d'une ville existante"""
    try:
        # L'URL dans la requête pointe vers un service nommé Nominatim OpenStreetMap, qui renvoie les informations
        # d'une ville selon certains paramètres (nom, longitude, etc...)

        # Structure de la reqûete :
        # q={city_name}: définit les paramètres (query de l'API), dans le cas ici, le nom de la ville
        # passé en parmètre

        # format=json : renvoie les infos en JSON
        # limit=1 : renvoie la première occurence de la recherche
        # accept-language=fr : renvoie les données en français

        # Pour raisons de sécurité, l'API exige un header User-Agent pour limiter les requêtes.
        # On passe le header défini au début du code dans la requête
        infos=requests.get(f'https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1&accept-language=fr', headers=headers)
        infos.raise_for_status()

        # Exemple d'une requête  : https://nominatim.openstreetmap.org/search?q=Paris&format=json&limit=1&accept-language=fr
        # Pour plus d'infos : https://nominatim.org/release-docs/develop/api/Search/

        # Récupération des données de la requéte
        name = infos.json()[0]['name']
        latitude = float(infos.json()[0]['lat'])
        longitude = float(infos.json()[0]['lon'])

        # On demande à l'API Open Meteo les relevés selon la latitude et la longitude
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&accept-language=fr,en')
        response.raise_for_status()
        json = response.json()

        # Création d'un dictionnaire avec les données
        new_city_data = {
            "nom":name,
            "latitude":json.get('latitude'),
            "longitude":json.get('longitude')
        }

        # On passe le dictionnaire dans une itération du modèle CityData pour pouvoir vérifier les types des données
        validate = city_data.CityData(**new_city_data)

        # On crée un dictionnaire avec le modèle Pydantic validé
        new_city=(validate.model_dump())

        # Interrogation du gesionnaire de la base de données pour insérer les informations
        db.insert_city_data(new_city['nom'], new_city['latitude'], new_city['longitude'])

        # La requête vers l'API Open Meteo renvoie dans le JSON un champ 'current_weather'
        # La variable ci-dessous récupère ce champ
        current_weather = json.get('current_weather')

        
        # Même processur qu'au-dessus pour insérer les relevés dans la base de données
        new_city_results={
            "temperature":current_weather.get('temperature'),
            "windspeed":current_weather.get('windspeed'),
            "time":current_weather.get('time')
        }

        # Validation des données avec Pydantic
        validate = wheather_response.WeatherResponseModel(**new_city_results)

        new_response=(validate.model_dump())
        db.insert_weather_results(new_city['nom'], new_response['temperature'], new_response['windspeed'], new_response['time'])
        return{"Succès dans la création"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur : {e}")