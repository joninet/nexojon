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

@router.get("/stock")
def stock (req: Request):
    verDB = FuncionesDB()
    producto= verDB.mostrarTabla("Producto")
    almacen= verDB.mostrarTabla("Almacen")
    return template.TemplateResponse("stock.html", {"request": req, "producto": producto, "almacen": almacen})

@router.post("/stock/ver")
async def stockVer(req: Request, 
                           producto_id: int = Form(None),
                           almacen_id: int = Form(None)
                           ):
    ver = FuncionesDB()
    stockActual = ver.obtenerStock(producto_id, almacen_id)
    info_mensaje = "Producto sin Stock en el amacen seleccionado" if not stockActual else "Producto"
    producto= ver.mostrarTabla("Producto")
    almacen= ver.mostrarTabla("Almacen")
    if not stockActual:
        return template.TemplateResponse("stock.html", {"request": req, "info_mensaje": info_mensaje, "producto": producto, "almacen": almacen})
    else:
        nombreProducto = str(ver.seleccionarDatos("Producto", producto_id)[0][1])
        umProducto = str(ver.seleccionarDatos("Producto", producto_id)[0][2])

        return template.TemplateResponse("stock.html", {"request": req, "info_mensaje": info_mensaje,
                                                        "stockActual": stockActual,
                                                        "nombreProducto": nombreProducto,
                                                        "umProducto": umProducto, "producto": producto, "almacen": almacen})
