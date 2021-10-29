from typing import Text
from peewee import *
from playhouse.flask_utils import FlaskDB
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = FlaskDB()

class User(UserMixin,db.Model):
    id=IntegerField(primary_key=True)
    Username = TextField()    
    contraseña = TextField() # validar si es necesario colocarla 
    rol = IntegerField() #0=ADMIN, 1=SUPERADMIN, 2=USUARIOS
    nombre= TextField()
    apellidos= TextField()
    email=TextField()
    direccion= TextField()
    celular=IntegerField()
    admin = BooleanField(default=False)

class Pedido(db.Model):
    id=TextField(primary_key=True)
    user= ForeignKeyField(User, backref="pedidos")
    fecha = DateField() # verificar si existe una funcion que genere la fecha automatica

class temporal(db.Model):
    nombre = TextField()
    descripcion = TextField()
    precio = IntegerField()
    cantidad= IntegerField()
    
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
    Usuario = ForeignKeyField(User,backref="platos")
    plato = ForeignKeyField(Platos,backref="pedidos")

class comentarios(db.Model):
    usuario=ForeignKeyField(User,backref="comentarios")
    plato=ForeignKeyField(Platos,backref="usuarios")
    comentario= TextField()


