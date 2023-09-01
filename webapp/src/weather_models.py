from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Unit(str, Enum):
    IMPERIAL = 'Imperial'
    METRIC = 'Metric'

class Timespan(str, Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"

class WeatherHour(BaseModel):
    time: datetime
    temp_c: float
    temp_f: float
    wind_mph: float
    wind_kph: float
    precip_mm: float
    precip_in: float
    is_future: bool

class WeatherTimeSeries(BaseModel):
    time: datetime
    temp: float
    wind_speed: float
    precip: float
    is_future: bool

class TimeseriesOptions(BaseModel):
    unit: Unit
    timespan: Timespan