from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Montar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar plantillas
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/equipos", response_class=HTMLResponse)
async def equipos(request: Request):
    return templates.TemplateResponse("equipos.html", {"request": request})

@app.get("/estadisticas", response_class=HTMLResponse)
async def estadisticas(request: Request):
    return templates.TemplateResponse("estadisticas.html", {"request": request})
