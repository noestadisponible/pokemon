from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
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
async def read_battles(request: Request):
    return templates.TemplateResponse("battles.html", {"request": request})
