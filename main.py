from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/pokedex", response_class=HTMLResponse)
async def read_pokedex(request: Request):
    return templates.TemplateResponse("pokedex.html", {"request": request})

@app.get("/trainers", response_class=HTMLResponse)
async def read_trainers(request: Request):
    return templates.TemplateResponse("trainers.html", {"request": request})

@app.get("/battles", response_class=HTMLResponse)
async def battles(request: Request):
    battle_links = [
        {
            "title": "Battle 1: Pikachu vs Charizard",
            "url": "https://youtu.be/7nDehONtCq4",
            "video_id": "7nDehONtCq4"
        },
        {
            "title": "Battle 2: Charmander vs Agumon",
            "url": "https://youtu.be/lfqVW-xWX0g?si=Y2gamOyr3HOXxiLK",
            "video_id": "lfqVW-xWX0g"
        },
        {
            "title": "Battle 3: Bulbasaur vs Skiploom",
            "url": "https://youtu.be/rqPfQgOEEeo?si=XR1Z4iAz2MQnSgj7",
            "video_id": "rqPfQgOEEeo"
        }
    ]
    return templates.TemplateResponse("battles.html", {"request": request, "battle_links": battle_links})


