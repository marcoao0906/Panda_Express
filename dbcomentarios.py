import sqlite3
from sqlite3 import Error

def conectar():
    dbname= 'db.sqlite3'
    conn= sqlite3.connect(dbname)
    return conn

def getcomen():
    conn= conectar()
    cursor= conn.execute("select * from comentarios;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def getcomenSecure(usuario_id):
    try : 
        conn= conectar()
        SQLstmt="select * from comentarios where usuario_id=?;"
        cursor= conn.execute(SQLstmt,  (usuario_id,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def addcomen(usuario_id, plato_id, comentario):
    try :
        conn=conectar()
        conn.execute("insert into comentarios (usuario_id, plato_id, comentario) values(?,?,?);", (usuario_id, plato_id,comentario))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def deleteComen(plato_id):
    try : 
        conn= conectar()
        SQLstmt="delete from comentarios where id='"+str(plato_id)+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado
    except Error as error:
        return error