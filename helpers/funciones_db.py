import sqlite3 as sql
import json
from fastapi import HTTPException
import math

class FuncionesDB():
  def __init__(self):
    self._con = sql.connect("./base_datos.db")
    self._cur = self._con.cursor()

  #funcion para insertar datos en una tabla
  #column: nombres de las columnas en formato lista column = ["name", "code"]
  #values: valores de la columna en formato lista values = ["valorName", "valorCode"]
  def insertarDatos(self, tabla, column, values):
    try:
      query = f"INSERT INTO {tabla} ({', '.join(column)}) VALUES ({', '.join(['?' for _ in values])})"
      self._cur.execute(query, values)
      self._con.commit()
      id_ = self._cur.lastrowid
      return id_
    except sql.Error as e:
      print(f"error: {e}")

  def editarRegistro(self, tabla, column, values, condition, conditionValues):
    try:
      setClause = ', '.join([f"{column} = ?" for column in column])
      query = f"UPDATE {tabla} SET {setClause} WHERE {condition}"

      values.extend(conditionValues)

      self._cur.execute(query, tuple(values))
      self._con.commit()
      return "corrrecto"
    
    except sql.Error as e:
        print(f"Error al actualizar datos: {e}")

  def seleccionarDatos(self, table, id):
    try:
      self._cur.execute(f"SELECT * FROM {table} WHERE id = ?", (id,))
      result = self._cur.fetchall()

      return result
    except sql.Error as e:
      print(f"Error al consultar datos: {e}")
      return None  
    
  def mostrarTabla(self, tabla):
    try:
      self._cur.execute(f"SELECT * FROM {tabla}")
      result = self._cur.fetchall()
      return result
    except sql.Error as e:
      print(f"Error al consultar datos: {e}")
      return None  
    
  def contarFilas(self, tabla):
    try:
        self._cur.execute(f"SELECT COUNT(*) FROM {tabla}")
        result = self._cur.fetchone()
        return result[0]
    except sql.Error as e:
        print(f"Error al contar filas: {e}")
        return 0
    
  def mostrarTablaPaginada(self, tabla, pagina, por_pagina):
    try:
        offset = (pagina - 1) * por_pagina
        self._cur.execute(f"SELECT * FROM {tabla} LIMIT {por_pagina} OFFSET {offset}")
        result = self._cur.fetchall()
        return result
    except sql.Error as e:
        print(f"Error al consultar datos paginados: {e}")
        return None
    
  def borrarDatos(self, tabla, id):
     try:
      self._cur.execute(f"DELETE FROM {tabla} WHERE id = ?", (id,))
      self._con.commit()
      return {"message": "Borrado correctamente"}
     except sql.Error as e:
       return {"message": f"Error al borrar: {e}"}
     
  def obtenerStock(self, producto_id, almacen_id):
      try:
          query = "SELECT cantidad FROM Stock WHERE producto_id = ? AND almacen_id = ?"
          self._cur.execute(query, (producto_id, almacen_id))
          result = self._cur.fetchone()
          if result:
              return result[0]  # Devuelve la cantidad
          else:
              return None  # Si no se encuentra ninguna fila con los criterios dados
      except sql.Error as e:
          print(f"Error al obtener cantidad: {e}")
          return None
      
  def editarStock(self, tabla, column, values, p_id, alm_id):
      try:
          setClause = ', '.join([f"{col} = ?" for col in column])
          query = f"UPDATE {tabla} SET {setClause} WHERE producto_id = ? AND almacen_id = ?"

          values.extend([p_id, alm_id])

          self._cur.execute(query, tuple(values))
          self._con.commit()
          return "corrrecto"
      except sql.Error as e:
          print(f"Error al actualizar datos: {e}")
          return None

  def __del__(self):
    self._con.close()
