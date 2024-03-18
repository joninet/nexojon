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

@router.get("/proveedores/nuevo", response_class=HTMLResponse)
def proveedoresNuevo(req:Request):
    return template.TemplateResponse("proveedores_nuevo.html", {"request": req})

@router.post("/proveedores/crear")
async def proveedoresCrear(req: Request, 
                           nombre: str = Form(None),
                           direccion: str = Form(None),
                           localidad: str = Form(None),
                           telefono: str = Form(None),
                           email: str = Form(None),
                           moneda: str = Form(None)
                           ):
    if not (nombre and direccion and localidad and telefono and email and moneda):
        error_msg = "Por favor, complete todos los campos."
        return template.TemplateResponse(
            "proveedores_nuevo.html", 
            {"request": req, "errorIngresoInsumo": error_msg, "nombre": nombre, "direccion": direccion, "localidad": localidad, "telefono": telefono, "email": email, "moneda": moneda}
        )
    fechaActual =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    column = ["nombre", "direccion", "localidad", "telefono", "email", "moneda", "fecha"]
    values = [nombre, direccion, localidad, telefono, email, moneda, fechaActual]

    insertar = FuncionesDB()
    insertar.insertarDatos("Proveedor", column, values)
    return template.TemplateResponse("datosActualizados.html", {"request": req})

@router.get("/Actualizado", response_class=HTMLResponse)
def index():
    return open("./templates/datosActualizados.html").read()

@router.delete("/proveedores/borrar/{proveedor_id}",)
def borrarProveedor(proveedor_id: int):
    verDB = FuncionesDB()
    producto_id_str = str(proveedor_id)
    borrar= verDB.borrarDatos("Proveedor", proveedor_id)
    return {"mensaje": "Proveedor eliminado correctamente"}

@router.get("/proveedores/editar/{proveedor_id}", response_class=HTMLResponse)
def editarProveedor(req: Request, proveedor_id: int):
    verDB = FuncionesDB()
    mostrarProveedor=verDB.seleccionarDatos("Proveedor", proveedor_id)
    return template.TemplateResponse("proveedores_editar.html", {"request": req, "mostrarProveedor": mostrarProveedor})

@router.post("/proveedores/editardb")
async def editarProveedor(req: Request,
                           id: int = Form(None),
                           nombre: str = Form(None),
                           direccion: str = Form(None),
                           localidad: str = Form(None),
                           telefono: str = Form(None),
                           email: str = Form(None),
                           moneda: str = Form(None)
                           ):

    if not (nombre and direccion and localidad and telefono and email and moneda):
        error_msg = "Por favor, complete todos los campos."
        verDB = FuncionesDB()
        return template.TemplateResponse(
            "datosNoActualizados.html", 
            {"request": req, "errorIngresoInsumo": error_msg, "nombre": nombre, "direccion": direccion, "localidad": localidad, "telefono": telefono, "email": email, "moneda": moneda}
        )

    column = ["nombre", "direccion", "localidad", "telefono", "email", "moneda"]
    values = [nombre, direccion, localidad, telefono, email, moneda]

    insertar = FuncionesDB()
    insertar.editarRegistro("Proveedor", column, values, f"id = ?", (id,))
    return template.TemplateResponse("datosActualizados.html", {"request": req})

@router.get("/proveedores/ver_todos")
def verProveedor(req:Request, page: int = 1):
    verDb = FuncionesDB()
    proveedores = verDb.mostrarTablaPaginada("Proveedor", page, 15)
    total_proveedor = verDb.contarFilas("Proveedor")
    total_paginas = math.ceil(total_proveedor / 15)
    return template.TemplateResponse("proveedores.html", { "request" : req, "proveedores": proveedores, "page": page, "total_paginas": total_paginas })

