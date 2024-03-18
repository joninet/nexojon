from fastapi import APIRouter, FastAPI, Request, Response, Form, Query, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from helpers.funciones_db import FuncionesDB
import datetime
import math
import sqlite3

router = APIRouter()

template = Jinja2Templates(directory="./templates")

@router.get("/estados/nuevo", response_class=HTMLResponse)
def estadoNuevo(req:Request):
    return template.TemplateResponse("estados_nuevo.html", {"request": req})

@router.post("/estados/crear")
async def estadoCrear(req: Request, 
                           nombre: str = Form(None)
                           ):
    if not (nombre):
        error_msg = "Por favor, complete todos los campos."
        return template.TemplateResponse(
            "estados_nuevo.html", 
            {"request": req, "errorIngreso": error_msg, "nombre": nombre}
        )

    column = ["nombre"]
    values = [nombre]

    insertar = FuncionesDB()
    insertar.insertarDatos("Estado", column, values)
    return template.TemplateResponse("datosActualizados.html", {"request": req})

@router.get("/Actualizado", response_class=HTMLResponse)
def index():
    return open("./templates/datosActualizados.html").read()

@router.delete("/estados/borrar/{estado_id}",)
def borrarEstado(estado_id: int):
    verDB = FuncionesDB()
    categoria_id_str = str(estado_id)
    borrar= verDB.borrarDatos("Estado", estado_id)
    return {"mensaje": "Estado eliminado correctamente"}

@router.get("/estados/ver_todos")
def verEstados(req:Request, page: int = 1):
    verDb = FuncionesDB()
    estados = verDb.mostrarTablaPaginada("Estado", page, 15)
    total_estados = verDb.contarFilas("Estado")
    total_paginas = math.ceil(total_estados / 15)
    return template.TemplateResponse("estados.html", { "request" : req, "estados": estados, "page": page, "total_paginas": total_paginas })
