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

def gettemSecure(username):
    try : 
        conn= conectar()
        SQLstmt="select * from temporal where usuario=?;"
        cursor= conn.execute(SQLstmt,  (username,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def addtem(nombre, descripcion, precio, cantidad, username):
    try :
        conn=conectar()
        conn.execute("insert into temporal (nombre, descripcion, precio, cantidad, usuario) values(?,?,?,?,?);", (nombre, descripcion, precio, cantidad, username))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def deletetem2(username):
    try : 
        conn= conectar()
        SQLstmt="delete from temporal where usuario='"+str(username)+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False
#para detalle pedidos

def deletetem(id):
    try : 
        conn= conectar()
        SQLstmt="delete from temporal where id='"+str(id)+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def gettem(id):
    try : 
        conn= conectar()
        SQLstmt="select * from temporal where id=?;"
        cursor= conn.execute(SQLstmt,  (id,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error
