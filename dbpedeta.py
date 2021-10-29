import sqlite3
from sqlite3 import Error

def conectar():
    dbname= 'db.sqlite3'
    conn= sqlite3.connect(dbname)
    return conn

def getDetallepedido():
    conn= conectar()
    cursor= conn.execute("select * from detallepedido;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def getDepedido(pedido_id):
    try : 
        conn= conectar()
        SQLstmt="select * from detallepedido where pedido_id=?;"
        cursor= conn.execute(SQLstmt,  (pedido_id,))
        resultado= cursor.fetchall()
        return resultado
    except Error as error:
        return error

def addPedidetalle(pedido_id, plato_id, cantidad):
    try :
        conn=conectar()
        conn.execute("insert into detallepedido (pedido_id, plato_id, cantidad) values(?,?,?);", (pedido_id, plato_id, cantidad))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def deletePedidetalle(pedido_id):
    try : 
        conn= conectar()
        SQLstmt="delete from detallepedido where pedido_id='"+str(pedido_id)+"';"
        print(SQLstmt)
        cursor= conn.execute(SQLstmt)
        resultado= cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado
    except Error as error:
        return error