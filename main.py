from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from fastapi import Form
from fastapi.responses import RedirectResponse

# Inicializar FastAPI
app = FastAPI()

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar plantillas
templates = Jinja2Templates(directory="templates")

# Configurar la conexión a la base de datos
database = mysql.connector.connect( # LLAMAMOS AL FUNCION CONNECT PARA CONECTARNOS
    host ='informatica.iesquevedo.es',
    port = 3333,
    ssl_disabled = True,
    user ='root', #USUARIO QUE USAMOS NOSOTROS
    password ='1asir', #CONTRASEÑA CON LA QUE NOS CONECTAMOS
    database='Lucho'
) 

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para la Pokédex
@app.get("/pokedex", response_class=HTMLResponse)
async def read_pokedex(request: Request):
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT idPokemon, nombre, descripcion, imagen FROM Pokemon")
    pokedex_list = cursor.fetchall()
    cursor.close()
    return templates.TemplateResponse("pokedex.html", {"request": request, "pokedex_list": pokedex_list})

# Ruta para la sección de entrenadores (estática)
@app.get("/trainers", response_class=HTMLResponse)
async def read_trainers(request: Request):
    # Aquí no usamos datos de la base de datos, devolvemos un HTML estático
    return templates.TemplateResponse("trainers.html", {"request": request})

# Ruta para editar
@app.get("/editar", response_class=HTMLResponse)
async def admin_page(request: Request):
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Pokemon")
    pokemon_list = cursor.fetchall()
    cursor.close()
    return templates.TemplateResponse("editar.html", {"request": request, "pokemon_list": pokemon_list})

# Añadir Pokémon
@app.post("/add_pokemon")
async def add_pokemon(nombre: str = Form(...), descripcion: str = Form(...), imagen: str = Form(...)):
    cursor = database.cursor()
    cursor.execute("INSERT INTO Pokemon (nombre, descripcion, imagen) VALUES (%s, %s, %s)", (nombre, descripcion, imagen))
    database.commit()
    cursor.close()
    return RedirectResponse("/editar", status_code=303)

# Eliminar Pokémon
@app.post("/delete_pokemon/{idPokemon}")
async def delete_pokemon(idPokemon: int):
    cursor = database.cursor()
    cursor.execute("DELETE FROM Pokemon WHERE idPokemon = %s", (idPokemon,))
    database.commit()
    cursor.close()
    return RedirectResponse("/editar", status_code=303)

# Formulario de edición
@app.get("/edit_pokemon/{idPokemon}", response_class=HTMLResponse)
async def edit_pokemon_form(request: Request, idPokemon: int):
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Pokemon WHERE idPokemon = %s", (idPokemon,))
    pokemon = cursor.fetchone()
    cursor.close()
    return templates.TemplateResponse("edit_pokemon.html", {"request": request, "pokemon": pokemon})

# Guardar cambios de edición
@app.post("/edit_pokemon/{idPokemon}")
async def save_edit_pokemon(idPokemon: int, nombre: str = Form(...), descripcion: str = Form(...), imagen: str = Form(...)):
    cursor = database.cursor()
    cursor.execute(
        "UPDATE Pokemon SET nombre = %s, descripcion = %s, imagen = %s WHERE idPokemon = %s",
        (nombre, descripcion, imagen, idPokemon)
    )
    database.commit()
    cursor.close()
    return RedirectResponse("/editar", status_code=303)
