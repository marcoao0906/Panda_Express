# BACKEND
# APLICACIÓN DE SERVIDOR

from typing import Any
from flask import Flask, render_template, redirect, request, jsonify,session,flash,url_for
from peewee import PeeweeException
from peewee import *
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager #utilizada para contener las conf. especificadas en login
from flask_login import current_user, UserMixin,login_user,logout_user,login_required
from models import *
from config import dev
from formulario import LoginForm
import dbplatos

app = Flask(__name__)
app.config.from_object(dev)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# crear lista de usuarios
usuarios=["admin@pandaexpress.com","laura@hotmail.com","jessica@yahoo.com","elder@yahoo.com","marcos@hotmail.com"]
contraseñas=["qwerty123","qwerty123","qwerty123","querty123","querty123","qwerty123"]


@app.route('/', methods=['GET'])
def inicio():
    return render_template('index.html')


@app.route('/qs', methods=['GET'])
def quienesomos():
    return render_template('quienesomos.html')


@app.route('/menu', methods=['GET'])
def menu():
    return render_template('menu.html')


@app.route('/login', methods=['GET'])
def login():
    forma=LoginForm()
    return render_template('login.html',form=forma)


# decorador para autenticar el usuario ingresado
@app.route("/autenticar/", methods=['GET', 'POST'])
def autenticar():  
    
    if request.method == 'POST':
        print(current_user)
        form=LoginForm()
        if form.validate_on_submit():
            username=request.form["username"]
            pswd=request.form["password"]        
            user=User.get(Username=username)
            if user:
                print(user.Username)
                print(user.contraseña)
            else:
                return redirect("/login")
               
            if user is not None and check_password_hash(user.contraseña, pswd):
                etiqueta=user.nombre
                if user.rol==1:
                    login_user(user,remember=form.remember_me.data)
                    print("current user:")
                    print (current_user)                
                    return render_template("dashboart.html",username=etiqueta)
                elif user.rol==2:
                    login_user(user,remember=form.remember_me.data)
                    print("current user:")
                    print (current_user)  
                    return render_template("busqueda.html",username=etiqueta)             
            else:
                return 'usuario o contraseña invalidos'
        return redirect("/login")
    return redirect("/login")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    print(current_user)
    return render_template("/index.html")

@app.route("/pagEliminarUsuario/")
def pageliminarUsuario():
    #query=Usuario.select(Usuario.Username)
    query=[]
    query=User.select(User.id,User.Username).where(User.rol!=1)
    print(query)
    #query=User.get(User.Username).where(User.rol!=1)
    #lista=list(query)
    #print(lista)
    #print(lista.Username)
    return render_template("eliminarusuario.html",lista=query)

@app.route("/crearUsuario/")
@login_required
def crearUsuario():
    return render_template("crearusuario.html")
    
@app.route("/nuevoUsuario/", methods=['GET', 'POST'])
def nuevo():
    if request.method=="POST":
        nuevo=request.form["email"]
        contraseña=request.form["password"]
        nombre=request.form["nombre"]
        apellido=request.form["apellido"]
        email=request.form["email"]
        rol=request.form["rol"]
        nuevo1=nuevo.split("@")
        nuevo2=nuevo1[0]
        #nuevo=nuevo1[0]
        if nuevo2=="admin":
            return redirect("/crearUsuario/")
        else:
            query=User.select().where(User.Username==nuevo)
            usuarios=list(query)
            if (len(usuarios)>0):
                print("ya existe un usuario "+nuevo)
                flash('Este usuario ya existe')
                return redirect("/crearUsuario/")
            else:
                print("puede registrarse")
                nuevoU=User.create(Username=nuevo,contraseña=generate_password_hash(contraseña, method='sha256'),rol=rol,nombre=nombre,apellidos=apellido,email=nuevo,direccion="Barranquilla",celular=30000000)
                print(nuevoU)        
                return render_template("busqueda.html",username=nuevo2)
    else:
        return redirect("/login")




@app.route("/eliminarUsuario/", methods=["GET", "POST"])
@login_required    
def eliminarUsuario(): 
    eliminar=request.form["eliminar"]
    query=User.delete().where(User.id==eliminar)
    query.execute()
    query=User.select(User.id).where(User.id!=1)
    lista=list(query)
    return render_template("eliminarusuario.html",lista=lista)


@app.route("/newregister/")           
def newregister():
    return render_template("registrarse.html")

@app.route("/registrarUsuario/",methods=['GET', 'POST'])
def registrarUsuario():
    if request.method=="POST":
        nuevo=request.form["email"]
        contraseña=request.form["password"]
        nombre=request.form["nombre"]
        apellido=request.form["apellido"]
        email=request.form["email"]
        nuevo1=nuevo.split("@")
        nuevo2=nuevo1[0]
        #nuevo=nuevo1[0]
        if nuevo2=="admin":
            return redirect("/newregister/")
        else:
            query=User.select().where(User.Username==nuevo)
            usuarios=list(query)
            if (len(usuarios)>0):
                print("ya existe un usuario "+nuevo)
                flash('Este usuario ya existe')
                return redirect("/newregister/")
            else:
                print("puede registrarse")
                nuevoU=User.create(Username=nuevo,contraseña=generate_password_hash(contraseña, method='sha256'),rol=2,nombre=nombre,apellidos=apellido,email=nuevo,direccion="Barranquilla",celular=30000000)
                print(nuevoU)        
                return render_template("busqueda.html",username=nuevo2)
    else:
        return redirect("/login")





# platos
platosasi1 = [
    ["Ramen", "18500", "muy rico", "10"],
    ["Arroz Frito", "23500", "super rico", "15"],
    ["Laksa", "23000", "rico", "18"],
    ["Pollo Tandoori", "26000", "delicios", "6"],
]


@app.route('/dashboart')
@login_required
def dashboartadm():
    return render_template('dashboart.html')


@app.route('/ConsuPla', methods=['GET', 'POST'])
def ConsuPla():
    # consultar platos
    plato = []
    nombreplato = request.args.get('Nombre')
    plato=dbplatos.getPlatosSecure(nombreplato)
    print(plato)
    return render_template('consultarpla.html', plato=plato)


@app.route('/VerPla', methods=['GET'])
def VerPla():
    # consultar platos
    plato = []
    platos = dbplatos.getPlatos()
    return render_template('consultarpla.html', platos=platos, plato=plato)


@app.route('/Agregapla', methods=['GET', 'POST'])
@login_required
def agregapla():
    # agregar platos
    platos=[]
    nombreplato = request.args.get('Nombre')
    precioplato = request.args.get('Precio')
    descripcionplato = request.args.get('Descripcion')
    #cantidadplato = request.args.get('Cantidad')
    secreo=dbplatos.addPlatos(nombreplato,descripcionplato,precioplato)
    if secreo:
        platos=dbplatos.getPlatos()
    else:
        platos=[]
    return render_template('agregarpla.html', platos=platos)


@app.route('/Eliminapla', methods=['GET', 'POST'])
@login_required
def Elimipla():
    # eliminar platos
    nombreplato = request.args.get('Nombre')
    plato = dbplatos.deletePlatos(nombreplato)
    plato=dbplatos.getPlatos()
    return render_template('eliminarpla.html', plato=plato)

#pedidos
@app.route('/dashboartusuario')
@login_required
def dashboartusuario():
    platos = dbplatos.getPlatos()
    return render_template('Busqueda.html', platos=platos)

#buscar platos usuario
@app.route('/buscapla', methods=['GET', 'POST'])
def buscapla():
    plato = []
    nombreplato = request.args.get('nombre')
    plato=dbplatos.getPlatosSecure(nombreplato)
    print(plato)
    return render_template('buscaplatos.html', plato=plato)

#Busca todos los platos desde el usuario final
@app.route('/VerPlausuario', methods=['GET'])
def VerPlausuario():
    # consultar platos
    plato = []
    platos = dbplatos.getPlatos()
    return render_template('buscaplatos.html', platos=platos, plato=plato)

#Añadir al carrito de compra desde el usuario final
@app.route('/Añadir',  methods=['GET', 'POST'])
@login_required
def añadir1():
    
    cantidad = request.args.get('cantidad')
    print(cantidad)
    return cantidad
    

@app.route('/Añadir/<string:id>',  methods=['GET', 'POST'])
@login_required
def añadir(id):
    cantidad = request.args.get('cantidad')
    print(cantidad)
        
    #listatem = list(dbplatos.getPlatosidsegure(id))
    #print(listatem)
    #print(listatem[0][1])
    #print(request.args.get('can'))
    #nombre= listatem[0][1]
    #descripcion= listatem[0][2]
    #precio= listatem[0][3]
    #cantidad =request.args.get('can')
    
    #alarma=dbtemp.addtem(nombre, descripcion, precio, cantidad)
    #if alarma:
    #    print("Ingreso")

    return id


#Añadir a favoritos desde el usuario final
@app.route('/Deseo/<string:id>')
@login_required
def favorito(id):
    print(id)
    return id

@app.route('/Comentarios/<string:id>')
@login_required
def Comentarios(id):
    print(id)
    return id
    

if __name__ == '__main__':
    app.run(debug=True, port=5500)