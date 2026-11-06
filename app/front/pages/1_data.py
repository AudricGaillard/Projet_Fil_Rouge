# Page Streamlit où les données de la base sont affichés 

import streamlit as st
import pandas as pd
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Récupération de l'URL de l'API FastAPI
url=os.getenv('API_URL')

# On va rechercher les données avec FastApi
st.write("# Données des villes")
response = requests.get(f"{url}/villes")

if response.status_code!=200:
    st.error("Erreur dans le chargement des données")
    st.stop()


data = response.json()

# Création d'un tableau de données avec Pandas
df = pd.DataFrame(data, columns=['nom', 'latitude', 'longitude', 'temperature','vitesse_vent', 'date_heure'])

# Affichage sur Streamlit
st.dataframe(df)

