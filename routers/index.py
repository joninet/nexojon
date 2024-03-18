from fastapi import APIRouter, FastAPI, Request, Response, Form, Query, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from helpers.funciones_db import FuncionesDB
import sqlite3

router = APIRouter()

template = Jinja2Templates(directory="./templates")

@router.get("/indexmain", response_class=HTMLResponse)
async def index(req: Request):
    verDb= FuncionesDB()
    categorias=verDb.mostrarTabla("Categoria")
    return template.TemplateResponse("index.html", {"request": req, "categorias": categorias})
