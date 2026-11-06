from pydantic import BaseModel, ValidationError

class WeatherResponseModel(BaseModel):
    temperature:float
    windspeed:float
    time:str


# Test unitaire pour la validation de données
if __name__ == "__main__":
    try:
        results=WeatherResponseModel(temperature=17.4, windspeed=30, time="2026-11-04T08:30")
        print(results)
    except ValidationError as e:
        print(e)
