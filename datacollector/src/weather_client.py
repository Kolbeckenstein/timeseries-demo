from datetime import datetime, timedelta
from dateutil.parser import parse
from enum import Enum
import requests
from os import environ

from .weather_models import WeatherHour

class ApiType(Enum):
    HISTORY = "history"
    FORECAST = "forecast"

def generate_base_call(api_type: ApiType) -> str:
    """Gets environment variables and concatenates them into the correct url to pull weather data from weatherapi.com.

    Requires:
    - WEATHER_API_KEY: An api key with weatherapi.com to allow api calls.
    - WEATHER_API_URL: Base host url for weatherapi
    - ZIP_CODE: the zip code to retrieve weather data for. Example: 70806
    """
    return (
        f"{environ['WEATHER_API_URL']}/v1/{api_type.value}.json?"
        f"key={environ['WEATHER_API_KEY']}&q={environ['ZIP_CODE']}"
    )

def raw_forecast_to_model(data: dict) -> list[WeatherHour]:
    """The history and forecast api calls both return a similarly shaped object, but we want to run this through a
    model for validation and clarity between layers. This reaches into the response body, finds the "hour" elements,
    and converts them into a standard pydantic model.
    """
    hours = []
    for forecast_day in data["forecast"]["forecastday"]:
        for hour in forecast_day["hour"]:
            hour_datetime = parse(hour["time"])
            hours.append(
                WeatherHour(
                    time=hour_datetime,
                    temp_c=hour["temp_c"],
                    temp_f=hour["temp_f"],
                    wind_mph=hour["wind_mph"],
                    wind_kph=hour["wind_kph"],
                    precip_mm=hour['precip_mm'],
                    precip_in=hour["precip_in"],
                    is_future=hour_datetime > datetime.now(),
                )
            )
    return hours

def fetch_json_and_translate(url: str) -> list[WeatherHour]:
    print(f"Requesting api data at {url}")
    json = requests.get(url).json()
    return raw_forecast_to_model(json)    

def get_historical_weather_hours(days = 14) -> list[WeatherHour]:
    """Retreives historical weather data, day by day, and returns a list of hour objects.
    Takes in a number of days to "look backward" through time, making an api call for each day, unioning
    the hours lists, and returning them as a single list.
    """
    hours = []
    for day_diff in range (days, -1, -1):
        now = datetime.now()
        delta = timedelta(days=day_diff)
        date = now - delta

        url = f"{generate_base_call(ApiType.HISTORY)}&dt={date.year}-{date.month}-{date.day}"
        hours = hours + fetch_json_and_translate(url)
    return hours

def get_forecast_hours(days = 10) -> list[WeatherHour]:
    """The forecast api returns hours for a range of days, all in one call. This grabs the default 10 days and
    returns them as hour objects.
    """
    url = f"{generate_base_call(ApiType.FORECAST)}&days={days}&aqi=no&alerts=no"
    return fetch_json_and_translate(url)
    