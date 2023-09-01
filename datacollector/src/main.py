from fastapi import FastAPI, Request
from fastapi import FastAPI

from .weather_client import get_historical_weather_hours, get_forecast_hours

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}



@app.get("/collect")
def collect_data():
    """ Collects historical, current, and forcast weather data from weatherapi.com, concatenating it into
        a single format and saving it to the timescale db.
    """
    weather_hours = get_historical_weather_hours() + get_forecast_hours()
    print(weather_hours)
    return 200