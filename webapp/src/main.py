from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI

from .weather_models import TimeseriesOptions

from .timescaledb_client import fetch_weather, fetch_timeseries_weather

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/")
def main_page(request: Request, response_class=HTMLResponse):
    """Landing spash page - contains contact information and a link to the chart."""
    return templates.TemplateResponse("main.html", {"request": request, "content": "welcome"})

@app.get("/content")
def content_page(request: Request, response_class=HTMLResponse):
    """Chart page - contains a line chart that displays weather data across recent history and near future forecast."""
    return templates.TemplateResponse("main.html", {"request": request, "content": "weather"})

@app.get("/api/weather_hours")
def get_weather_hours(request: Request):
    """General endpoint that gives a full reply of stored weather data."""
    return fetch_weather() 

@app.post("/api/weather_timeseries")
def weather_timeseries(timeseries_options: TimeseriesOptions):
    return fetch_timeseries_weather(timeseries_options)

