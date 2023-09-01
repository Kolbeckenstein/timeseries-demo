from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI

from .timescaledb_client import fetch_weather

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/")
def main_page(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/content")
def content_page(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("content.html", {"request": request})

@app.get("/api/weather_hours")
def get_weather_hours(request: Request):
    return fetch_weather() 



# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}