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

@router.get("/categorias/nuevo", response_class=HTMLResponse)
def categoriasNuevo(req:Request):
    return template.TemplateResponse("categorias_nuevo.html", {"request": req})

@router.post("/categorias/crear")
async def categoriasCrear(req: Request, 
                           nombre: str = Form(None)
                           ):
    if not (nombre):
        error_msg = "Por favor, complete todos los campos."
        return template.TemplateResponse(
            "categorias_nuevo.html", 
            {"request": req, "errorIngreso": error_msg, "nombre": nombre}
        )

    column = ["nombre"]
    values = [nombre]

    insertar = FuncionesDB()
    insertar.insertarDatos("Categoria", column, values)
    return template.TemplateResponse("datosActualizados.html", {"request": req})

@router.get("/Actualizado", response_class=HTMLResponse)
def index():
    return open("./templates/datosActualizados.html").read()

@router.delete("/categorias/borrar/{categoria_id}",)
def borrarCategoria(categoria_id: int):
    verDB = FuncionesDB()
    categoria_id_str = str(categoria_id)
    borrar= verDB.borrarDatos("Categoria", categoria_id)
    return {"mensaje": "Proveedor eliminado correctamente"}

@router.get("/categorias/ver_todos")
def verProductos(req:Request, page: int = 1):
    verDb = FuncionesDB()
    categorias = verDb.mostrarTablaPaginada("Categoria", page, 15)
    total_categorias = verDb.contarFilas("Categoria")
    total_paginas = math.ceil(total_categorias / 15)
    return template.TemplateResponse("categorias.html", { "request" : req, "categorias": categorias, "page": page, "total_paginas": total_paginas })
