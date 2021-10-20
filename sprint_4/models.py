from typing import Text
from peewee import *
from playhouse.flask_utils import FlaskDB

db = FlaskDB()

class Usuario(db.Model):
    Username = TextField(primary_key=True)    
    contraseña = TextField() # validar si es necesario colocarla 
    rol = IntegerField() #0=ADMIN, 1=SUPERADMIN, 2=USUARIOS
    nombre= TextField()
    apellidos= TextField()
    email=TextField()
    direccion= TextField()
    celular=IntegerField()

class Pedido(db.Model):
    id=TextField(primary_key=True)
    user = ForeignKeyField(Usuario, backref="usuarios")
    fecha = IntegerField() # verificar si existe una funcion que genere la fecha automatica

class Platos(db.Model):
    id=AutoField(primary_key=True)    
    nombre = TextField()
    descripcion = TextField()
    precio = IntegerField()
    
    # imagenes agregar de acuerdo al plato (ojo!!!!!!)    

class detallePedido(db.Model):
    pedido=ForeignKeyField(Pedido)
    plato = ForeignKeyField(Platos)
    cantidad=IntegerField()

class deseo(db.Model):
    Usuario = ForeignKeyField(Usuario)
    plato = ForeignKeyField(Platos)

