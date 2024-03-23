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

@router.get("/movimiento/nuevo", response_class=HTMLResponse)#indica que la ruta va a responder con contenido html
def nuevoMovimiento(req: Request):
  verDB = FuncionesDB()
  categorias= verDB.mostrarTabla("Categoria")
  producto= verDB.mostrarTabla("Producto")
  proveedor= verDB.mostrarTabla("Proveedor")
  estado= verDB.mostrarTabla("Estado")
  almacen= verDB.mostrarTabla("Almacen")
  usuario= verDB.mostrarTabla("Usuario")
  #print(categorias)
  return template.TemplateResponse("movimiento_nuevo.html", {"request": req, "categorias": categorias, "producto": producto, "proveedor": proveedor, "estado": estado, "almacen": almacen, "usuario": usuario})

@router.post('/movimiento/crear')
async def crearMovimiento(
    req: Request,
    producto_id: int = Form(None),
    cantidad: float = Form(None),
    usuario_id: int = Form(None),
    tipo_movimieto: str = Form(None),
    almacen_origen_id: int = Form(None),
    almacen_destino_id: int = Form(None)):

    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    column = ["producto_id", "cantidad", "usuario_id", "almacen_origen_id", "almacen_destino_id", "tipo_movimieto", "fecha"]
    values = [producto_id, cantidad, usuario_id, almacen_origen_id, almacen_destino_id, tipo_movimieto, fecha_actual]

    insertar = FuncionesDB()
    insertar.insertarDatos("Movimientos", column, values)

    #descuento stock
    stockActual=insertar.obtenerStock(producto_id, almacen_origen_id)

    if not stockActual:
      columnStock=["cantidad","producto_id", "almacen_id"]
      valuesStock=[cantidad, producto_id, almacen_origen_id]
      error_msg="El almacen de origen no cuenta con la cantidad pedida"
      return template.TemplateResponse("movimiento_nuevo.html", {"request": req, "errorIngresoInsumo": error_msg})
    else:
      stockNuevo=float(stockActual) - cantidad
      columnStock=["cantidad"]
      valuesStock=[stockNuevo]
      insertar.editarStock("Stock", columnStock, valuesStock, producto_id, almacen_origen_id)

    #ingreso Stock
    stockActualDestino=insertar.obtenerStock(producto_id, almacen_destino_id)
    if not stockActualDestino:
      columnStockIngreso=["cantidad","producto_id", "almacen_id"]
      valuesStockIngreso=[cantidad, producto_id, almacen_destino_id]
      insertar.insertarDatos("Stock", columnStockIngreso, valuesStockIngreso)
    else:
      stockNuevoDestino = cantidad + float(stockActualDestino)
      columnStockDestino=["cantidad"]
      valuesStockDestino=[stockNuevoDestino]
      insertar.editarStock("Stock", columnStockDestino, valuesStockDestino, producto_id, almacen_destino_id)

    verDB = FuncionesDB()
    categorias= verDB.mostrarTabla("Categoria")
    producto= verDB.mostrarTabla("Producto")
    proveedor= verDB.mostrarTabla("Proveedor")
    estado= verDB.mostrarTabla("Estado")
    almacen= verDB.mostrarTabla("Almacen")
    usuario= verDB.mostrarTabla("Usuario")
    info_mensaje = "El movimiento fue creado exitosamente"
    return template.TemplateResponse("movimiento_nuevo.html", {"request": req, "info_mensaje": info_mensaje, "categorias": categorias, "producto": producto, "proveedor": proveedor, "estado": estado, "almacen": almacen, "usuario": usuario})