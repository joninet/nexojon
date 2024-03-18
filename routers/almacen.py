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

@router.get("/almacen/nuevo", response_class=HTMLResponse)
def almacenNuevo(req:Request):
    return template.TemplateResponse("almacen_nuevo.html", {"request": req})

@router.post("/almacen/crear")
async def almacenCrear(req: Request, 
                           nombre: str = Form(None)
                           ):
    if not (nombre):
        error_msg = "Por favor, complete todos los campos."
        return template.TemplateResponse(
            "almacen_nuevo.html", 
            {"request": req, "errorIngreso": error_msg, "nombre": nombre}
        )

    column = ["nombre"]
    values = [nombre]

    insertar = FuncionesDB()
    insertar.insertarDatos("Almacen", column, values)
    return template.TemplateResponse("datosActualizados.html", {"request": req})

@router.get("/Actualizado", response_class=HTMLResponse)
def index():
    return open("./templates/datosActualizados.html").read()

@router.delete("/almacen/borrar/{estado_id}",)
def borraralmacen(estado_id: int):
    verDB = FuncionesDB()
    categoria_id_str = str(estado_id)
    borrar= verDB.borrarDatos("Almacen", estado_id)
    return {"mensaje": "Estado eliminado correctamente"}

@router.get("/almacen/ver_todos")
def verAlmacen(req:Request, page: int = 1):
    verDb = FuncionesDB()
    almacen = verDb.mostrarTablaPaginada("Almacen", page, 15)
    total_almacen = verDb.contarFilas("Almacen")
    total_paginas = math.ceil(total_almacen / 15)
    return template.TemplateResponse("almacen.html", { "request" : req, "almacen": almacen, "page": page, "total_paginas": total_paginas })
