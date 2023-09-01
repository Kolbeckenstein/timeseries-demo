from fastapi import FastAPI, Request
from fastapi import FastAPI

from .weather_service import get_weather_history

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}



@app.get("/collect")
def collect_data():
    """ Collects historical and forcast weather data from weatherapi.com, concatenating it into
        a single format and saving it to the timescale db.
    """
    return 200