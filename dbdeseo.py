import sqlite3
from sqlite3 import Error

def conectar():
    dbname= 'db.sqlite3'
    conn= sqlite3.connect(dbname)
    return conn

def getdeseo():
    conn= conectar()
    cursor= conn.execute("select * from deseo;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def getdeseoSecure(usuario_id):
    try : 
        conn= conectar()
        SQLstmt="select * from deseo where usuario_id=?;"
        cursor= conn.execute(SQLstmt,  (usuario_id,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def addDeseo(usuario_id, plato_id, descripcion):
    try :
        conn=conectar()
        conn.execute("insert into deseo (usuario_id, plato_id, descripcion) values(?,?,?);", (usuario_id, plato_id,descripcion))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def deleteDeseo(plato_id):
    try : 
        conn= conectar()
        SQLstmt="delete from deseo where id='"+str(plato_id)+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado
    except Error as error:
        return error