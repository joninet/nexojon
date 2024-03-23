from fastapi import APIRouter, FastAPI, Request, Response, Form, Query, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from helpers.funciones_db import FuncionesDB
from datetime import datetime
import math
import sqlite3

router = APIRouter()

template = Jinja2Templates(directory="./templates")

@router.get("/ingresos/nuevo", response_class=HTMLResponse)#indica que la ruta va a responder con contenido html
def nuevoProducto(req: Request):
  verDB = FuncionesDB()
  categorias= verDB.mostrarTabla("Categoria")
  producto= verDB.mostrarTabla("Producto")
  proveedor= verDB.mostrarTabla("Proveedor")
  estado= verDB.mostrarTabla("Estado")
  almacen= verDB.mostrarTabla("Almacen")
  usuario= verDB.mostrarTabla("Usuario")
  #print(categorias)
  return template.TemplateResponse("ingresos_nuevo.html", {"request": req, "categorias": categorias, "producto": producto, "proveedor": proveedor, "estado": estado, "almacen": almacen, "usuario": usuario})

@router.post('/ingresos/crear')
async def crearIngreso(
    req: Request,
    producto_id: int = Form(None),
    cantidad: float = Form(None),
    proveedor_id: int = Form(None),
    oc: str = Form(None),
    lote: str = Form(None),
    vto: str = Form(None),
    estado_id: int = Form(None),
    remito: str = Form(None),
    usuario_id: int = Form(None),
    almacen_id: int = Form(None)):

    verDB = FuncionesDB()
    producto=verDB.seleccionarDatos("Producto",producto_id)
    proveedor=verDB.seleccionarDatos("Proveedor",proveedor_id)
    estado=verDB.seleccionarDatos("Estado", estado_id)
    usuario=verDB.seleccionarDatos("Usuario", usuario_id)
    almacen=verDB.seleccionarDatos("Almacen", almacen_id)

    if not producto or not proveedor or not estado or not usuario or not almacen:
      error_msg = "Codigo inexistente"
      return template.TemplateResponse(
          "ingresos_nuevo.html", 
          {"request": req, "errorIngresoInsumo": error_msg, "producto_id": producto_id, "cantidad": cantidad, "proveedor_id": proveedor_id, "oc": oc, "lote": lote, "vto": vto, 
          "estado_id": estado_id, "remito": remito, "usuario_id": usuario_id, "almacen_id": almacen_id}
      )


    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    column = ["producto_id", "cantidad", "proveedor_id", "oc", "lote", "vto", "estado_id", "remito", "usuario_id", "almacen_id", "fecha"]
    values = [producto_id, cantidad, proveedor_id, oc, lote, vto, estado_id, remito, usuario_id, almacen_id, fecha_actual]

    columnStock = ["producto_id", "cantidad", "almacen_id"]
    valuesStock = [producto_id, cantidad, almacen_id]

    insertar = FuncionesDB()
    insertar.insertarDatos("Ingresos", column, values)
    insertar.insertarDatos("Stock", columnStock, valuesStock)
<<<<<<< HEAD
    return template.TemplateResponse("datosActualizados.html", {"request": req})
=======

    verDB = FuncionesDB()
    categorias= verDB.mostrarTabla("Categoria")
    producto= verDB.mostrarTabla("Producto")
    proveedor= verDB.mostrarTabla("Proveedor")
    estado= verDB.mostrarTabla("Estado")
    almacen= verDB.mostrarTabla("Almacen")
    usuario= verDB.mostrarTabla("Usuario")
    info_mensaje = "El Ingreso fue creado exitosamente"

    return template.TemplateResponse("ingresos_nuevo.html", {"request": req, "info_mensaje": info_mensaje, "categorias": categorias, "producto": producto, "proveedor": proveedor, "estado": estado, "almacen": almacen, "usuario": usuario})
>>>>>>> e7c8a88 (OK)

@router.get("/ingresos/ver_todos")
def verIngresos(req:Request, page: int = 1):
    verDb = FuncionesDB()
    ingresos = verDb.mostrarTablaPaginada("Ingresos", page, 15)
    total_ingresos = verDb.contarFilas("Ingresos")
    total_paginas = math.ceil(total_ingresos / 15)

    producto = verDb.mostrarTabla("Producto")
    proveedor = verDb.mostrarTabla("Proveedor")
    estado = verDb.mostrarTabla("Estado")
    usuario = verDb.mostrarTabla("Usuario")
    usuario = verDb.mostrarTabla("Usuario")
    almacen =  verDb.mostrarTabla("Almacen")

    return template.TemplateResponse("ingresos.html", { "request" : req, "ingresos": ingresos, "producto": producto, "proveedor": proveedor, 
                                                        "estado": estado, "usuario": usuario, 
                                                        "almacen": almacen, "page": page, "total_paginas": total_paginas })

@router.delete("/ingresos/borrar/{ingresos_id}",)
def borrarIngreso(ingresos_id: int):
    verDB = FuncionesDB()
    producto_id_str = str(ingresos_id)
    borrar= verDB.borrarDatos("Ingresos", ingresos_id)
    return {"mensaje": "Producto eliminado correctamente"}

@router.get("/ingresos/editar/{ingresos_id}", response_class=HTMLResponse)
def editarIngreso(req: Request, ingresos_id: int):

    verDB = FuncionesDB()
    mostrarIngreso=verDB.seleccionarDatos("Ingresos", ingresos_id)

    if not mostrarIngreso:
        return template.TemplateResponse("id_inexistente.html", {"request": req})
    else:
        categorias= verDB.mostrarTabla("Categoria")
        producto= verDB.mostrarTabla("Producto")
        proveedor= verDB.mostrarTabla("Proveedor")
        estado= verDB.mostrarTabla("Estado")
        almacen= verDB.mostrarTabla("Almacen")
        usuario= verDB.mostrarTabla("Usuario")

        return template.TemplateResponse("ingresos_editar.html", {"request": req, "mostrarIngreso": mostrarIngreso, "categorias": categorias, "producto": producto, "proveedor": proveedor, "estado": estado, "almacen": almacen, "usuario": usuario})

@router.post("/ingresos/editardb/{ingresos_id}")
async def editarIngresos(
    req: Request,
    ingresos_id: int,
    oc: str = Form(None),
    lote: str = Form(None),
    vto: str = Form(None),
    remito: str = Form(None),
    cantidad: str = Form(None),
    producto_id: int = Form(None),
    proveedor_id: int = Form(None),
    estado_id: int = Form(None),
    usuario_id: int = Form(None),
    almacen_id: int = Form(None)):

    verDB = FuncionesDB()
    producto=verDB.seleccionarDatos("Producto",producto_id)
    proveedor=verDB.seleccionarDatos("Proveedor",proveedor_id)
    estado=verDB.seleccionarDatos("Estado", estado_id)
    usuario=verDB.seleccionarDatos("Usuario", usuario_id)
    almacen=verDB.seleccionarDatos("Almacen", almacen_id)

    if not producto or not proveedor or not estado or not usuario or not almacen:
        error_msg = "Codigo inexistente"
        return template.TemplateResponse(
            "ingresos_nuevo.html", 
            {"request": req, "errorIngresoInsumo": error_msg, "producto_id": producto_id, "cantidad": cantidad, "proveedor_id": proveedor_id, "oc": oc, "lote": lote, "vto": vto, 
            "estado_id": estado_id, "remito": remito, "usuario_id": usuario_id, "almacen_id": almacen_id}
        )

    column = ["oc", "lote", "vto", "remito", "cantidad", "producto_id", "proveedor_id", "estado_id", "usuario_id", "almacen_id"]
    values = [oc, lote, vto, remito, cantidad, producto_id, proveedor_id, estado_id, usuario_id, almacen_id]

    insertar = FuncionesDB()
    insertar.editarRegistro("Ingresos", column, values, f"id = ?", (ingresos_id,))
<<<<<<< HEAD
    return template.TemplateResponse("datosActualizados.html", {"request": req})
=======
    info_mensaje = "El Ingreso fue creado exitosamente"
    return template.TemplateResponse("ingresos_editar.html", {"request": req, "info_mensaje": info_mensaje})
>>>>>>> e7c8a88 (OK)
