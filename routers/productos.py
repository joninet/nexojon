from fastapi import APIRouter, FastAPI, Request, Response, Form, Query, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from helpers.funciones_db import FuncionesDB
import math
import sqlite3

router = APIRouter()

template = Jinja2Templates(directory="./templates")



@router.get("/", response_class=HTMLResponse)
async def read_root():
    return template.TemplateResponse("index.html", {"request": "request"})

@router.get("/productos/nuevo", response_class=HTMLResponse)#indica que la ruta va a responder con contenido html
def nuevoProducto(req: Request):
  verDB = FuncionesDB()
  categorias= verDB.mostrarTabla("Categoria")
  #print(categorias)
  return template.TemplateResponse("productos_nuevo.html", {"request": req, "categorias": categorias})

@router.get("/Actualizado", response_class=HTMLResponse)
def index():
    return open("./templates/datosActualizados.html").read()

@router.delete("/productos/borrar/{producto_id}",)
def borrarProducto(producto_id: int):
    verDB = FuncionesDB()
    producto_id_str = str(producto_id)
    borrar= verDB.borrarDatos("Producto", producto_id)
    return {"mensaje": "Producto eliminado correctamente"}

@router.get("/productos/editar/{producto_id}", response_class=HTMLResponse)
def editarProducto(req: Request, producto_id: int):
    verDB = FuncionesDB()
    mostrarProducto=verDB.seleccionarDatos("Producto", producto_id)

    if not mostrarProducto:
        return template.TemplateResponse("id_inexistente.html", {"request": req})
    else:
        categorias= verDB.mostrarTabla("Categoria")
        return template.TemplateResponse("productos_editar.html", {"request": req, "mostrarProducto": mostrarProducto, "categorias": categorias})

@router.post("/productos/editardb")
async def editarProducto(
    req: Request,
    id:int = Form(None),
    nombre: str = Form(None),
    um: str = Form(None),
    descripcion: str = Form(None),
    categoria_id: int = Form(None)):

    if not (nombre and um and descripcion and categoria_id):
        error_msg = "Por favor, complete todos los campos."
        verDB = FuncionesDB()
        categorias= verDB.mostrarTabla("Categoria")
        return template.TemplateResponse(
            "datosNoActualizados.html", 
            {"request": req, "errorIngresoInsumo": error_msg, "nombre": nombre, "um": um, "descripcion": descripcion, "categoria_id": categoria_id, "categorias": categorias}
        )

    column = ["nombre", "um", "descripcion", "categoria_id"]
    values = [nombre, um, descripcion, categoria_id]

    insertar = FuncionesDB()
    insertar.editarRegistro("Producto", column, values, f"id = ?", (id,))
    return template.TemplateResponse("datosActualizados.html", {"request": req})

@router.post('/productos/crear')
async def crearProducto(
    req: Request,
    nombre: str = Form(None),
    um: str = Form(None),
    descripcion: str = Form(None),
    categoria_id: int = Form(None)):

    if not (nombre and um and descripcion and categoria_id):
        error_msg = "Por favor, complete todos los campos."
        verDB = FuncionesDB()
        categorias= verDB.mostrarTabla("Categoria")
        return template.TemplateResponse(
            "productos_nuevo.html", 
            {"request": req, "errorIngresoInsumo": error_msg, "nombre": nombre, "um": um, "descripcion": descripcion, "categoria_id": categoria_id, "categorias": categorias}
        )

    column = ["nombre", "um", "descripcion", "categoria_id"]
    values = [nombre, um, descripcion, categoria_id]
    insertar = FuncionesDB()
    producto_id = insertar.insertarDatos("Producto", column, values)

    column_stock = ["producto_id", "cantidad", "almacen_id"]
    values_stock = [producto_id, 0, "almacen"]
    insertar.insertarDatos("Stock", column_stock, values_stock)

    return template.TemplateResponse("datosActualizados.html", {"request": req})

@router.get("/productos/ver_todos")
def verProductos(req:Request, page: int = 1):
    verDb = FuncionesDB()
    productos = verDb.mostrarTablaPaginada("Producto", page, 15)
    total_productos = verDb.contarFilas("Producto")
    total_paginas = math.ceil(total_productos / 15)
    categorias = verDb.mostrarTabla("Categoria")
    return template.TemplateResponse("productos.html", { "request" : req, "productos": productos, "categorias": categorias, "page": page, "total_paginas": total_paginas })
