from pydantic import BaseModel, ValidationError

class CityData(BaseModel):
    """Classe représentant les données d'une ville (son nom, sa latitude, et sa longitude)."""
    nom : str
    latitude : float
    longitude : float


# Test unitaire pour la validation de données
if __name__ == "__main__":
    try:
        city=CityData(nom='Paris', latitude=48.853382, longitude=2.355208)
        print(city)
    except ValidationError as e:
        print(e)