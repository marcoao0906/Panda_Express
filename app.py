# BACKEND
# APLICACIÓN DE SERVIDOR

from typing import Any
from flask import Flask, render_template, redirect, request, jsonify,session,flash,url_for
from peewee import PeeweeException
from peewee import *
import sqlite3
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager #utilizada para contener las conf. especificadas en login
from flask_login import current_user, UserMixin,login_user,logout_user,login_required
from sqlite3 import Error
from models import *
from config import dev
from formulario import LoginForm
import dbplatos
import dbpedeta
import dbtemp
import dbdeseo
import random
import dbpedido
import dbcomentarios
from datetime import datetime

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
contrasenas=["qwerty123","qwerty123","qwerty123","querty123","querty123","qwerty123"]


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
    if current_user.is_authenticated and current_user.admin==True :
        return redirect("/")
    elif current_user.is_authenticated and current_user.admin==False:
        return render_template("busqueda.html")
    else:
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
                print(user.contrasena)
                session['username']=username
                session['rol']=user.rol

            else:
                return redirect("/login")
               
            if user is not None and check_password_hash(user.contrasena, pswd):
                etiqueta=user.nombre
                if user.rol==1 or user.rol==2:
                    login_user(user,remember=form.remember_me.data)
                    print("current user:")
                    print (current_user)                
                    return render_template("dashboart.html",username=current_user)
                elif user.rol==3:
                    login_user(user,remember=form.remember_me.data)
                    print("current user:")
                    print (current_user)  
                    return render_template("busqueda.html",username=etiqueta)             
            else:
                return 'usuario o contrasena invalidos'
        return redirect("/login")
    return redirect("/login")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    print(current_user)
    return redirect("/")

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

def crearUsuario():
    #prueba=True
    if current_user.is_authenticated and current_user.admin==True:
     #prueba:
        print("current en crear")
        print(current_user)
        return render_template("registro.html")
    elif current_user.is_authenticated and current_user.admin==False:
    #elif prueba:
        return render_template("busqueda.html")
    else:
        return redirect("/") 
#*********************************************ACTUALIZAR USUARIOS****************************
@app.route("/actualizarUsuario/<username>")
@login_required
def actualizarUsuario(username=None):
    print(username,"el de actualizar")
    user=User.get(Username=username)
    return render_template("actualizarUsuarios.html",nombre=user.nombre,apellidos=user.apellidos,email=user.email,username=user.Username,direccion=user.direccion,celular=user.celular)

@app.route("/actualizar/", methods=["POST","GET"])
@login_required
def actualizar():
    if request.method =="POST":
        
        query = User.update(nombre=request.form["nombre"],apellidos=request.form["apellidos"],email=request.form["email"],Username=request.form["username"],direccion=request.form["direccion"],celular=request.form["celular"]).where(User.Username==request.form["username"])
        query.execute() 
        return redirect("/gestionUsuario")


    
@app.route("/nuevoUsuario/", methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method=="POST":
        nombre=request.form["nombre"]
        apellido=request.form["apellidos"]
        email=request.form["email"]
        username=request.form["username"]
        direccion=request.form["direccion"]
        contrasena=request.form["contrasena"]        
        celular=request.form["celular"]
        rol=request.form["rol"]
        nuevo1=email.split("@")
        nuevo2=nuevo1[0]
        admin=0
        if nombre!=""and apellido!=""and email!=""and username!=""and direccion!=""and contrasena!=""and celular!=""and rol!="":
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
                    nuevoU=User.create(id=random.randrange(100000,999999,1),nombre=nombre,apellidos=apellido,email=email,Username=email,contrasena=generate_password_hash(contrasena, method='sha256'),rol=rol,direccion=direccion,celular=celular,admin=admin)
                    print(nuevoU)   
                    print(current_user.Username) 
                    etiqueta=(current_user.nombre)
                    etiqueta=etiqueta
                    return redirect("/gestionUsuario/")
        else:
            return redirect("/gestionUsuario/")            
    else:
        return redirect("/gestionUsuario/")



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
    return render_template("registrarse.html")

@app.route("/registrarUsuario/",methods=['GET', 'POST'])

def registrarUsuario():
    
    if request.method=="POST":
        nuevo=request.form["email"]
        contrasena=request.form["password"]
        nombre=request.form["nombre"]
        apellido=request.form["apellido"]
        email=request.form["email"]
        celular=request.form["celular"]
        direccion=request.form["direccion"]
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
                nuevoU=User.create(id=random.randrange(100000,999999,1),Username=nuevo,contrasena=generate_password_hash(contrasena, method='sha256'),rol=3,nombre=nombre,apellidos=apellido,email=nuevo,direccion=direccion,celular=celular)
                print(nuevoU)        
                return render_template("busqueda.html",username=nuevo2)
    else:
        return redirect("/login")


#***********************gestion de usuarios********************************
@app.route("/gestionUsuario/")
@login_required
def gestionUsuario():
    print(current_user,"desde gestion antes de todo")
    if session['rol']==1 or session['rol']==2:
        nameuser=session["username"]
        return render_template("gestionUsuarios.html",nameuser=nameuser)
    else:
        return redirect("/logout")

"""
    if  current_user.is_authenticated and current_user.admin==True:
        nameuser=session["username"]
        return render_template("gestionUsuarios.html",nameuser=nameuser)        
    elif current_user.is_authenticated and current_user.admin==False:
        return redirect("/")
    print(current_user,"esto es en gestion usuarios")
"""      
    

#***********************buscar un usuario*************************************
@app.route("/buscaUsuario/", methods=["GET", "POST"])
@login_required
def buscausuario():
    if request.method =="POST":
        prueba=True
        #if current_user.is_authenticated and current_user.admin==True:
        if prueba:
            buscar=request.form["nombreU"]
            print(buscar)
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
        #elif current_user.is_authenticated and current_user.admin==False:
        elif prueba:
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
    
    
    return render_template("gestionUsuarios.html",username=user.Username,id=user.id,direccion=user.direccion,contrasena=user.contrasena, nombre=user.nombre,apellidos=user.apellidos,email=user.email,celular=user.celular,rol=tipoUsu)





#*********************************************platos***********************

#platos

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
    if session['rol']==1 or session['rol']==2:
        #nameuser=session["username"]
        nombreplato = request.args.get('Nombre')
        plato = dbplatos.deletePlatos(nombreplato)
        plato=dbplatos.getPlatos()
        return render_template('eliminarpla.html', plato=plato)

        #return render_template("gestionUsuarios.html",nameuser=nameuser)
    else:
        return redirect("/logout")
    
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
    

@app.route('/Anadir/<int:id>/',  methods=['GET', 'POST'])
@login_required
def añadir(id):
    cantidad=int(request.args.get('cantidad'))
    listatem = list(dbplatos.getPlatosidSecure(id))
    nombre= listatem[0][1]
    descripcion= listatem[0][2]
    precio= listatem[0][3]
    username=session['username']
    print(username)
    alarma=dbtemp.addtem(nombre, descripcion, precio, cantidad, username)
    if alarma:
        mensaje="Tu pedidos se encuentra en el Carrito de Compras"
    else:
        mensaje="Tu Pedido no se Gestiono Vuelve a Intentar"

    return render_template('buscaplatos.html', mensaje=mensaje)



@app.route('/pedidopla')
@login_required
def pedidopla():
    listapedi=list(dbtemp.gettemSecure(session['username']))
    print(listapedi)
    total=0
    for i in range(0,len(listapedi),1):
        multi=(int(listapedi[i][4])*int(listapedi[i][3]))
        print(multi)
        total=total+multi
        
    return render_template('carrocom.html',listapedi=listapedi, total=total )

@app.route('/pedidopla/<string:id>/',  methods=['GET', 'POST'])
@login_required
def eliminarpedido(id):
    alarma=dbtemp.deletetem(id)
    if alarma:
        mensaje="Se Elimino Correctamente el Pedido"
    else:
        mensaje="No se Elimino el Pedido, Intente de Nuevo"
    return render_template('carrocom.html',mensaje=mensaje )


@app.route('/pedido/<string:id>',  methods=['GET', 'POST'])
@login_required
def detallepedido(id):
    idpedido=str(random.randrange(1000,9999,1))
    print(idpedido)
    print(id)
    username=session['username']
    print(username)
    listapedi=list(dbtemp.gettemporal())
    print(listapedi)
    for i in range(0,len(listapedi),1):
        plato=listapedi[i][1]
        cantidad=int(listapedi[i][4])
        print(type(plato))
        print(type(cantidad))
        men=cantidad
        dbpedeta.addPedidetalle(idpedido,plato,cantidad)
    fecha=datetime.today()
    pedido=dbpedido.addPedido(idpedido,username,id,fecha)

    if pedido:
        men='Su Pedido se Gestionó con ¡¡¡EXITO!!'
    else:
        men='Su Pedio NO pudo ser Gestionado'

    dbtemp.deletetem2(username)
    return render_template('carrocom.html',men=men )
    


#Añadir a favoritos desde el usuario final

@app.route('/Deseo/<string:id>',  methods=['GET', 'POST'])
@login_required
def favorito(id):
    listatem=dbplatos.getPlatosidSecure(id)
    nombre= listatem[0][1]
    descripcion= listatem[0][2]
    username=session['username']
    alarma=dbdeseo.addDeseo(username, nombre, descripcion)
    if alarma:
        mensaje="Tu Plato se encuentra en Lista de Deseos"
    else:
        mensaje="Tu Plato no se Añadio a la Lista de Deseos"
    pladeseos=dbdeseo.getdeseoSecure(username)
    return render_template('deseos.html',pladeseos=pladeseos,mensaje=mensaje)

@app.route('/eliminardeseo/<string:id>', methods=['GET', 'POST'])
@login_required
def eliminardeseo(id):
    username=session['username']
    alarma=dbdeseo.deleteDeseo(id)
    if alarma:
        mensaje="Tu Plato se encuentra en Lista de Deseos"
    else:
        mensaje="Tu Plato no se Añadio a la Lista de Deseos"
    pladeseos=dbdeseo.getdeseoSecure(username)
    return render_template('deseos.html',pladeseos=pladeseos,mensaje=mensaje)




@app.route('/Comentarios/<string:id>/', methods=['GET', 'POST'])
@login_required
def Comentarios(id):
    listatem=dbplatos.getPlatosidSecure(id)
    nombre= listatem[0][1]
    comentario=request.args.get('comentario')
    username=session['username']
    alarma=dbcomentarios.addcomen(username, nombre, comentario)
    if alarma:
        mensaje="Tu Plato se encuentra en Lista de Deseos"
    else:
        mensaje="Tu Plato no se Añadio a la Lista de Deseos"
    platospedido=dbcomentarios.getcomenSecure(username)
    return render_template('comentarios.html',platospedido=platospedido,mensaje=mensaje)



@app.route('/eliminarcomen/<string:id>', methods=['GET', 'POST'])
@login_required
def eliminarcomen(id):
    username=session['username']
    alarma=dbcomentarios.deleteComen(id)
    if alarma:
        mensaje="Tu Plato se encuentra en Lista de Deseos"
    else:
        mensaje="Tu Plato no se Añadio a la Lista de Deseos"
    platospedido=dbcomentarios.getcomenSecure(username)
    return render_template('comentarios.html',platospedido=platospedido,mensaje=mensaje)

@app.route('/listadeseos')
@login_required
def listadeseos():
    username=session['username']
    pladeseos=dbdeseo.getdeseoSecure(username)
    return render_template('deseos.html',pladeseos=pladeseos)
    

@app.route('/comentarios')
@login_required
def comentariopla():
    username=session['username']
    platospedido=dbcomentarios.getcomenSecure(username)
    return render_template('comentarios.html',platospedido=platospedido)

if __name__ == '__main__':
    app.run(debug=True, port=5500)