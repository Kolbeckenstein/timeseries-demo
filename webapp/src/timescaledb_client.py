from datetime import datetime
import psycopg2
import pytz

from .weather_models import TimeseriesOptions, Timespan, Unit, WeatherHour, WeatherTimeSeries

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
        
def fetch_timeseries_weather(timeseries_options: TimeseriesOptions) -> None:
    """Fetches data, grouping by either day or hour, and returns it in either imperial or metric units.
    
    There is currently a bug! This query doesn't roll up to days the way it should. There will be some duplicates for the moment.
    """
    conn = psycopg2.connect("")
    cursor = conn.cursor()
    query = f"""SELECT time_bucket('1 {'day' if timeseries_options.timespan == Timespan.DAILY else 'hour'}', time) AS time, 
            {'avg(temp_c)' if timeseries_options.unit == Unit.METRIC else 'avg(temp_f)'} as temp,
            {'avg(wind_kph)' if timeseries_options.unit == Unit.METRIC else 'avg(wind_mph)'} as wind,
            {'avg(precip_mm)' if timeseries_options.unit == Unit.METRIC else 'avg(precip_in)'} as precip
            FROM weather_hour
            GROUP BY time
            ORDER BY time ASC;
            """
    print(query)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    #This is a hacky workaround due to a bug in how the time bucketed day data comes back.
    #Days are currently returning as 24 hourly buckets, each with the beginning of the day as time.
    #For brevity, just deduping the results with a dictionary to mimic the intended effect.
    dedupe_dict = {}
    for result in results:
        if result[0] not in dedupe_dict:
            dedupe_dict[result[0]] = result
    results = dedupe_dict.values()

    return [
        WeatherTimeSeries(
            time=result[0],
            temp=result[1],
            wind_speed=result[2],
            precip=result[3],
            is_future=result[0] > datetime.utcnow().replace(tzinfo=pytz.utc),
        ) for result in results
    ]