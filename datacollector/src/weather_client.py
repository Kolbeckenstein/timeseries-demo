from datetime import datetime
import requests
from os import environ

def get_historical_weather(date: datetime) -> dict:
    