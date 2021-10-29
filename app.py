# BACKEND
# APLICACIÓN DE SERVIDOR

from typing import Any
from flask import Flask, render_template,abort, redirect, request, jsonify,session,flash,url_for
from peewee import PeeweeException
from peewee import *
import sqlite3
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from playhouse.shortcuts import model_to_dict
from flask_login import LoginManager,current_user, UserMixin,login_user,logout_user,login_required
from sqlite3 import Error
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
    print(user_id,"hjkgjkgjgjhgjhjh")
    return User.get(user_id)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"),404


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
    if current_user.is_authenticated and current_user.admin==True:
        return redirect("/gestionUsuario/")
    elif current_user.is_authenticated and current_user.admin==False:
        return render_template("busqueda.html")
    else:
        forma=LoginForm()
        return render_template('login.html',form=forma)


# decorador para autenticar el usuario ingresado
@app.route("/autenticar/", methods=['GET', 'POST'])
def autenticar(): 
    print("current user desde autenticar",current_user) 
    if current_user.is_authenticated:
    		return redirect(url_for("login"))
    
    if request.method == 'POST':
        print(current_user)
        form=LoginForm()
        if form.validate_on_submit():
            username=request.form["username"]
            pswd=request.form["password"]  
                  
            user=User.get(Username=username)
            if user is None:
                raise NotFound(username)
                #abort(404)
            
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
                    session["username"]=username
                    next_page = request.args.get('next')
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page = url_for('gestionUsuario')#gestionUsuario
                        return redirect(next_page)               
                    return redirect("/gestionUsuario/")
                elif user.rol==3:
                    login_user(user,remember=form.remember_me.data)
                    print("current user:")
                    print (current_user)  
                    session["username"]=current_user.Username
                    return render_template("busqueda.html",username=session["username"])             
            else:
                return 'usuario o contraseña invalidos'
        return redirect("/login")
    return redirect("/login")


#***********************gestion de usuarios********************************
@app.route("/gestionUsuario/")
@login_required
def gestionUsuario():
    print(current_user,"desde gestion antes de todo")
    if  current_user.is_authenticated and current_user.admin==True:
        nameuser=session["username"]
        return render_template("gestionUsuarios.html",nameuser=nameuser)        
    elif current_user.is_authenticated and current_user.admin==False:
        return redirect("/")
    print(current_user,"esto es en gestion usuarios")
    

#***********************buscar un usuario*************************************
@app.route("/buscaUsuario/", methods=["GET", "POST"])
@login_required
def buscausuario():
    if request.method =="POST":
        if current_user.is_authenticated and current_user.admin==True:
            buscar=request.form["nombreU"]
            busqueda=User.select(User.id,User.Username,User.nombre).where(User.Username==buscar)
            lista=list(busqueda)
            print(list(lista))
        
            dbname="db.sqlite3"
            conn= sqlite3.connect(dbname)
            cursor= conn.execute("select id,username,nombre from User where username=?;",(buscar,))
            resultados= list(cursor.fetchall())
            if len(resultados)==0:
                flash('Este usuario no existe')
            else:
                conn.close()
                return render_template("gestionUsuarios.html",lista=resultados,nameuser=current_user.Username)                   
        elif current_user.is_authenticated and current_user.admin==False:
            return redirect("/")        
    return redirect("/gestionUsuario/")


@app.route("/datos/<username>")
def datos(username=None):
    print("current user desde hipervinculo")    
    print(current_user)
    
    user=User.get(Username=username)
    if user.rol==3:
        tipoUsu="cliente"
    elif user.rol==2:
        tipoUsu="administrador"
    elif user.rol==1:
         tipoUsu="Super-Admin"

    print(user.Username ,"esta es la lista get")
    
    
    return render_template("gestionUsuarios.html",username=user.Username,id=user.id,direccion=user.direccion,contrasena=user.contraseña, nombre=user.nombre,apellidos=user.apellidos,email=user.email,celular=user.celular,rol=tipoUsu)









        


#*****************************LOGOUT******************************************
@app.route("/logout")
@login_required
def logout():
    logout_user()
    print(current_user)
    return redirect("/")

#*******************************Pagina para eliminar usuarios***************************
"""
@app.route("/pagEliminarUsuario/<username>")
def pageliminarUsuario(username=None):
    print("current user desde boton eliminar usuario")    
    print(current_user)
    
    user=User.get(Username=username)
    if user.rol==3:
        tipoUsu="cliente"
    elif user.rol==2:
        tipoUsu="administrador"
    elif user.rol==1:
         tipoUsu="Super-Admin"

    print(user.Username ,"esta es la lista get")
    
    
    return render_template("eliminarusuario2.html",username=user.Username,id=user.id,direccion=user.direccion,contrasena=user.contraseña, nombre=user.nombre,apellidos=user.apellidos,email=user.email,celular=user.celular,rol=tipoUsu)
"""


















#*****************************************************crear un usuario desde la sesion del administrador
@app.route("/crearUsuario/")
@login_required
def crearUsuario():
    if current_user.is_authenticated and current_user.admin==True:
        print("current en crear")
        print(current_user)
        return render_template("registro.html")
    elif current_user.is_authenticated and current_user.admin==False:
        return render_template("busqueda.html")
    else:
        return redirect("/")    
    
@app.route("/nuevoUsuario/", methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method=="POST":
        nombre=request.form["nombre"]
        apellido=request.form["apellidos"]
        email=request.form["email"]
        username=request.form["username"]
        direccion=request.form["direccion"]
        contraseña=request.form["contrasena"]        
        celular=request.form["celular"]
        rol=request.form["rol"]
        nuevo1=email.split("@")
        nuevo2=nuevo1[0]
        admin=0
        if nombre!=""and apellido!=""and email!=""and username!=""and direccion!=""and contraseña!=""and celular!=""and rol!="":
            #nuevo=nuevo1[0]
            print(rol,"este es el rol")
            if rol=="Administrador":
                rol=2
                admin=True
            elif rol=="Cliente":
                rol=3
                admin=False
        
            if nuevo2=="admin":
                return redirect("/gestionUsuario/")
            else:            
                query=User.select().where(User.Username==username)
                usuarios=list(query)
                if (len(usuarios)>0):
                    print("ya existe un usuario "+nuevo2)
                    flash('Este usuario ya existe')
                    return redirect("/gestionUsuario/")
                else:
                    print(admin)
                    print("puede registrarse")
                    nuevoU=User.create(nombre=nombre,apellidos=apellido,email=email,Username=email,contraseña=generate_password_hash(contraseña, method='sha256'),rol=rol,direccion=direccion,celular=celular,admin=admin)
                    print(nuevoU)   
                    print(current_user.Username) 
                    etiqueta=(current_user.nombre)
                    etiqueta=etiqueta
                    return redirect("/gestionUsuario/")
        else:
            return redirect("/gestionUsuario/")            
    else:
        return redirect("/gestionUsuario/")


#**************************************eliminar usuarios*****************************************

@app.route("/eliminarUsuario/<username>", methods=["GET", "POST"])
@login_required    
def eliminarUsuario(username=None):
    if request.method == "POST":
        print("current? desde eliminar")
        print(current_user) 
        #eliminar=request.form["eliminar"]    
        #query=User.delete().where(User.id==eliminar)
        #query.execute()
        #query=User.select(User.Username).where(User.rol!=1)
        #lista=list(query)

        #query=User.select(User.id).where(User.id!=1)
        print("este es el username",username)
        user=User.get(Username=username)    
        print(user.Username)

        query=User.delete().where(User.Username==username)
        query.execute()
     
        return redirect("/gestionUsuario")
    return redirect("/gestionUsuario")


@app.route("/newregister/")           
def newregister():
    return render_template("registrar.html")
#******************************************REGISTRAR USUARIO DESDE LOGIN*************
@app.route("/registrarUsuario/",methods=['GET', 'POST'])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["nombre"]
        apellido=request.form["apellidos"]
        email=request.form["email"]
        
        direccion=request.form["direccion"]
        contraseña=request.form["contrasena"]        
        celular=request.form["celular"]
        if nombre=="" and apellido==""and email==""and direccion==""and contraseña=="" and celular=="":
            flash('llenar todos los campos')
            return redirect("/login")
        else:        
            nuevo1=email.split("@")
            nuevo2=nuevo1[0]
            #nuevo=nuevo1[0]
        
        
            if nuevo2=="admin":
                return redirect("/gestionUsuario/")
            else:            
                query=User.select().where(User.Username==email)
                usuarios=list(query)
                if (len(usuarios)>0):
                    print("ya existe un usuario "+nuevo2)
                    flash('Este usuario ya existe')
                    return redirect("/login")
                else:                
                    print("puede registrarse")
                    nuevoU=User.create(nombre=nombre,apellidos=apellido,email=email,Username=email,contraseña=generate_password_hash(contraseña, method='sha256'),rol=3,direccion=direccion,celular=celular,admin=0)
                    print(nuevoU)   
                    print(current_user.Username) 
                    etiqueta=(current_user.nombre)
                    etiqueta=etiqueta
                    return redirect("/login")
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
    print("current en dash board")
    print(current_user)    
    return render_template('dashboart.html',username=current_user.Username)


@app.route('/ConsuPla', methods=['GET', 'POST'])
def ConsuPla():
    print("current user desde consupla")
    print(current_user) 
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
    print("desde buscar plato")
    print(current_user)
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