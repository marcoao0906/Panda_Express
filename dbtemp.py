import sqlite3
from sqlite3 import Error

def conectar():
    dbname= 'db.sqlite3'
    conn= sqlite3.connect(dbname)
    return conn

def gettemporal():
    conn= conectar()
    cursor= conn.execute("select * from temporal;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def gettemSecure(nombre):
    try : 
        conn= conectar()
        t= (nombre)
        SQLstmt="select * from temporal where nombre=?;"
        cursor= conn.execute(SQLstmt,  (nombre,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def addtem(nombre, descripcion, precio, cantidad):
    try :
        conn=conectar()
        conn.execute("insert into temporal (nombre, descripcion, precio, cantidad) values(?,?,?);", (nombre, descripcion, precio, cantidad))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def deletetem(nombre):
    try : 
        conn= conectar()
        SQLstmt="delete from temporal where nombre='"+str(nombre)+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado
    except Error as error:
        return error
#para detalle pedidos
def gettem(id):
    try : 
        conn= conectar()
        SQLstmt="select * from temporal where id=?;"
        cursor= conn.execute(SQLstmt,  (id,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error
