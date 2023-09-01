import psycopg2

from .weather_models import WeatherHour

def fetch_weather() -> None:
    conn = psycopg2.connect("")
    cursor = conn.cursor()
    query = "SELECT * FROM weather_hour;"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return [
        WeatherHour(
            time = result[0],
            temp_c=result[1],
            temp_f=result[2],
            wind_mph=result[3],
            wind_kph=result[4],
            precip_mm=result[5],
            precip_in=result[6],
            is_future=result[7]
        ) for result in results
    ]
        