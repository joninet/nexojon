from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from helpers.funciones_db import FuncionesDB
from routers.productos import router as productRouter
from routers.index import router as index
from routers.proveedores import router as proveedorRouter
from routers.categorias import router as categoriaRouter
from routers.estados import router as estadosRouter
from routers.ingresos import router as ingresosRouter
from routers.almacen import router as almacenRouter
from routers.movimiento import router as movimientoRouter
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(productRouter)
app.include_router(index)
app.include_router(proveedorRouter)
app.include_router(categoriaRouter)
app.include_router(estadosRouter)
app.include_router(ingresosRouter)
app.include_router(almacenRouter)
app.include_router(movimientoRouter)


app.mount("/templates/static", StaticFiles(directory="templates/static"), name="static")





