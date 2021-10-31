import sqlite3
from sqlite3 import Error

def conectar():
    dbname= 'db.sqlite3'
    conn= sqlite3.connect(dbname)
    return conn


def addPedido(id, user_id, valor, fecha):
    try :
        conn=conectar()
        conn.execute("insert into pedido (id, user_id, total, fecha) values(?,?,?,?);", (id, user_id, valor, fecha))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def getpedido():
    conn= conectar()
    cursor= conn.execute("select * from pedido;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados