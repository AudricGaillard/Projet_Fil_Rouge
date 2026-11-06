# Page de formulaire pour ajouter une nouvelle ville dans la base

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

url=os.getenv('API_URL')

st.write("# Ajouter une ville")

# Création du formulaire
with st.form("City Form"):
    st.write("Ajouter une ville")

    # Champ de texte
    city_name = st.text_input("Nom de la ville")

    # Bouton pour soumettre les données
    submit = st.form_submit_button("Envoyer")

    # Si le bouton est cliqué
    if submit:

        # Envoie du nom entré dans le formulaire vers FastApi
        response = requests.post(f"{url}/ville/add", params={"city_name":city_name})

        # Si la requête renvoie autre que 201 pour le code statut
        if response.status_code!=201:
            st.error("Erreur : la ville est déjà dans la base de données.")
            st.stop()

        # Sinon
        else:
            st.success("Succés !")
            st.balloons()   