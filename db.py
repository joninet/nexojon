import sqlite3

conn = sqlite3.connect('App_Stock3/base_datos.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE Movimientos (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 fecha DATE NOT NULL,
                 cantidad REAL NOT NULL,
               
                 producto_id INTEGER NOT NULL,
                 usuario_id INTEGER NOT NULL,
                 almacen_id INTEGER NOT NULL,
               
                 FOREIGN KEY (producto_id) REFERENCES Producto(id)
                 FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                 FOREIGN KEY (almacen_id) REFERENCES Almacen(id)
               
                 
               )
               """)


conn.commit()
conn.close()

