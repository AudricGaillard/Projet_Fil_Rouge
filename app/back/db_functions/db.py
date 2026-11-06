# Script de gestion de la base de données

import sqlite3
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

# Pour avoir le chemin de la base de données SQLite depuis le fichier .env
path=os.getenv('DB_PATH')

def init_db():
    """Initialise (ou réinitialise) la base de données avec les tables."""
    try:
        conn = sqlite3.connect(f'{path}')
    
        cur = conn.cursor()

        cur.executescript("""
            DROP TABLE IF EXISTS villes;
            DROP TABLE IF EXISTS releves;
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS villes (
                id INTEGER PRIMARY KEY,
                nom TEXT UNIQUE NOT NULL,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL 
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS releves (
                id INTEGER PRIMARY KEY,
                ville_id INTEGER UNIQUE NOT NULL,
                temperature FLOAT NOT NULL,
                vitesse_vent FLOAT NOT NULL,
                date_heure TEXT NOT NULL,
                FOREIGN KEY (ville_id)
                REFERENCES villes (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
        """)
    except Exception as e:
        print(e)
    finally:
        conn.close()


def insert_city_data (city_name:str, city_latitude:float, city_longitude:float):
    """Insère de nouvelles données dans les tables"""
    try:
        conn = sqlite3.connect(f'{path}')

        cur = conn.cursor()

        # Afin de bien faire comprendre à Python les variables étant des chaînes de caractères, on met
        # par exemple city_name entre guillemets dans la requête.
        cur.execute(f"""
            INSERT INTO villes (nom, latitude, longitude)
            VALUES ('{city_name}', {city_latitude}, {city_longitude});
        """)


        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur : {e}")
    finally:
        conn.close()



def insert_weather_results(city_name:str, city_temperature:float, city_windspeed:float, date:str):
    """Insère les relevés météo d'une ville"""
    try:
        conn = sqlite3.connect(f'{path}')

        cur = conn.cursor()

        # Plutôt que d'écrire WHERE nom ='{city_name}', on utilise LIKE
        id = cur.execute(f"""
            SELECT id FROM villes
            WHERE nom LIKE '%{city_name}%';
        """).fetchall()

        # Ici, id vaut [(1,)], on récupère la valeur dans le tuple ainsi : 
        city_id = id[0][0]
         

        cur.execute(f"""
            INSERT INTO releves (ville_id, temperature, vitesse_vent, date_heure)
            VALUES ({city_id}, {city_temperature}, {city_windspeed}, '{date}');
        """)
        
        conn.commit()        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        conn.close()


def get_weather_results():
    try:
        conn = sqlite3.connect(f'{path}')

        cur = conn.cursor()

        data = cur.execute(f"""
            SELECT nom, latitude, longitude, temperature, vitesse_vent, date_heure FROM villes
            LEFT JOIN releves
                ON villes.id=releves.ville_id;
        """)
        return data.fetchall()
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()