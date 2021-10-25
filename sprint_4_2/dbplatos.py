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
        SQLstmt="select * from platos where nombre=?;"
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
        return True
    except Error as error:
        print(error)
        return False

def deletePlatos(nombre):
    try : 
        conn= conectar()
        SQLstmt="delete from platos where nombre='"+str(nombre)+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado
    except Error as error:
        return error


