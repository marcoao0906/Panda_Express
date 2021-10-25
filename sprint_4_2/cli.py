from app import *
from playhouse.shortcuts import model_to_dict
from datetime import date, time,datetime 

@app.cli.command("datos_iniciales")
def datos_iniciales():
    db.init_app(app)
    u0=User.get_or_create(id=10,Username="admin@pandaexpress.com", contraseña=generate_password_hash("qwerty"), rol=1, nombre="admin", apellidos="admin",email="admin@pandaexpress.com",direccion="Barranquilla",celular=300000000)

    
app.cli()
