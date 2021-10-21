import sqlite3
from sqlite3 import Error

def conectar():
    dbname= 'db.sqlite3'
    conn= sqlite3.connect(dbname)
    return conn

def getPlatos():
    conn= conectar()
    cursor= conn.execute("select * from platos;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def getPlatosSecure(nombre):
    try : 
        conn= conectar()
        t= (nombre)
        SQLstmt="select * from Producto where nombre=?;"
        cursor= conn.execute(SQLstmt,  (nombre,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def addPlatos(nombre, descripcion, precio):
    try :
        conn=conectar()
        conn.execute("insert into platos (nombre, descripcion, precio) values(?,?,?);", (nombre, descripcion, precio))
        conn.commit()
        conn.close()
        print("entro")
        return True
    except Error as error:
        print(error)
        return False

