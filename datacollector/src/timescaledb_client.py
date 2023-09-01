import psycopg2

from .weather_models import WeatherHour

def attempt_create_table_if_not_exists():
    #Creates a connection to local timescaledb by connecting to underlying postgresdb using environment variables
    conn = psycopg2.connect("")

    # create weather data hypertable
    query_create_weather_hour_table = """CREATE TABLE IF NOT EXISTS weather_hour (
                                            time TIMESTAMPTZ NOT NULL,
                                            temp_c decimal,
                                            temp_f decimal,
                                            wind_mph decimal,
                                            wind_kph decimal,
                                            precip_mm decimal,
                                            precip_in decimal,
                                            is_future boolean,
                                            UNIQUE (time)
                                        );
                                        """

    query_create_hypertable =  "SELECT create_hypertable('weather_hour', 'time', if_not_exists => TRUE);"

    cursor = conn.cursor()
    cursor.execute(query_create_weather_hour_table)
    cursor.execute(query_create_hypertable)
    # commit changes to the database to make changes persistent
    conn.commit()
    cursor.close()

def insert_weather_hours(weather_hours: list[WeatherHour]) -> None:
    conn = psycopg2.connect("")
    cursor = conn.cursor()
    for hour in weather_hours:
        try:
            insert_query = f"""
                INSERT INTO weather_hour
                (time, temp_c, temp_f, wind_mph, wind_kph, precip_mm, precip_in, is_future)
                VALUES
                ('{hour.time}', {hour.temp_c}, {hour.temp_f}, {hour.wind_mph}, {hour.wind_kph}, {hour.precip_mm}, {hour.precip_in}, '{"true" if hour.is_future else "false"}')
                ON CONFLICT (time) DO UPDATE
                SET temp_c = excluded.temp_c,
                temp_f = excluded.temp_f,
                wind_mph = excluded.wind_mph,
                wind_kph = excluded.wind_kph,
                precip_mm = excluded.precip_mm,
                precip_in = excluded.precip_in,
                is_future = excluded.is_future
                ;
            """
            cursor.execute(insert_query)
        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
    conn.commit()
    cursor.close()
    print(f"Attempted to save {len(weather_hours)} records.")
    
