from datetime import datetime
from pydantic import BaseModel

class WeatherHour(BaseModel):
    time: datetime
    temp_c: float
    temp_f: float
    wind_mph: float
    wind_kph: float
    precip_mm: float
    precip_in: float
    is_future: bool