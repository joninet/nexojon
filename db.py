import sqlite3 as sql
class FuncionesDB():
    def __init__(self):
        self._con = sql.connect("App_Stock3/base_datos.db")
        self._cur = self._con.cursor()

    def borrarRegistrosTabla(self, tabla):
        try:
            query = f"DELETE FROM {tabla}"
            self._cur.execute(query)
            self._con.commit()
            print("Se han borrado todos los registros de la tabla.")
        except sql.Error as e:
            print(f"Error: {e}")

    def borrarTabla(self, tabla):
        try:
            query = f"DROP TABLE IF EXISTS {tabla}"
            self._cur.execute(query)
            self._con.commit()
            print(f"La tabla {tabla} ha sido eliminada.")
        except sql.Error as e:
            print(f"Error: {e}")

    def __del__(self):
        self._con.close()

# Crear una instancia de la clase FuncionesDB
db = FuncionesDB()
db.borrarRegistrosTabla("Stock")



