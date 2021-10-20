# BACKEND
# APLICACIÓN DE SERVIDOR

from typing import Any
from flask import Flask, render_template, redirect, request, jsonify
from peewee import PeeweeException

#from playhouse.shortcuts import model_to_dict

from models import *
from config import dev


app = Flask(__name__)
app.config.from_object(dev)
db.init_app(app)


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
    return render_template('login.html')


# decorador para autenticar el usuario ingresado
@app.route("/autenticar/", methods=['GET', 'POST'])
def autenticar():
    #verificar metodo de envio y determinar si es un usuario registrado
    if request.method =="POST":
        username = request.form["user"]
        clave = request.form["pwd"]
        sw=0
        i=0
        while i<len(usuarios) and sw==0:            
            if usuarios[i] ==username:
                userid=username.split("@")
                userid1=userid[0]
                #renderizar al perfil de administrador de sistema
                if userid1=="admin":
                    if clave==contraseñas[i]:
                        #renderizar al perfil de usuario cliente 
                        sw=1            
                        return render_template("dashboart.html",username=userid1)
                    else:
                        return redirect("/login")                                          
                if clave==contraseñas[i]:                                           
                    sw=1
                    return render_template("busqueda.html", username=userid1)
                else:
                    return redirect("/login")
            else:
                i+=1 
        #renderizar a login si el usuario no esta registrado                   
        if sw==0:
           return redirect("/newregister/")
    #renderizar a login si el metodo es GET
    else:
        return redirect("/login")


@app.route("/pagEliminarUsuario/")
def pageliminarUsuario():
    return render_template("eliminarusuario.html",lista=usuarios)

@app.route("/eliminarUsuario/", methods=["GET", "POST"])    
def eliminarUsuario(): 
    eliminar=request.form["eliminar"]
    sw=0
    i=0
    while i<len(usuarios) and sw==0:
        if usuarios[i]==eliminar:
            indice=i
            usuarios.pop(indice)
            contraseñas.pop(indice)
            sw=1
            return render_template("dashboart.html")
        else:
            i+=1
        
    return render_template ("dashboart.html")


@app.route("/newregister/")           
def newregister():
    return render_template("registrarse.html")

@app.route("/registrarUsuario/",methods=['GET', 'POST'])
def registrarUsuario():
    if request.method=="POST":
        nuevo=request.form["email"]
        nuevo1=nuevo.split("@")
        nuevo2=nuevo1[0]
        #nuevo=nuevo1[0]
        if nuevo2=="admin":
            return redirect("/newregister/")
        else:
            i=0
            sw=0
            while i<len(usuarios) and sw==0:
                if usuarios[i]==nuevo:
                    #nuevo1=random.randint(1, 9999999)
                    #nuevo=nuevo + str(nuevo1)
                    #usuarios.append(nuevo)
                    #contraseñas.append(request.form("textarea"))
                    return redirect("/newregister/")
                    sw=1
                    #return render_template("busqueda.html",username=nuevo)
                
                else:
                    i+=1
        usuarios.append(nuevo)
        psw=request.form["textarea"]
        contraseñas.append(psw)
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
def dashboartadm():
    return render_template('dashboart.html')


@app.route('/ConsuPla', methods=['GET', 'POST'])
def ConsuPla():
    # consultar platos
    plato = []
    nombreplato = request.args.get('Nombre')
    print("si entro")
    for i in range(len(platosasi1)):
        if nombreplato == platosasi1[i][0]:
            
            Nombre = platosasi1[i][0]
            Precio = platosasi1[i][1]
            Descripcion = platosasi1[i][2]
            Cantidad = platosasi1[i][3]
            plato = [Nombre, Precio, Descripcion, Cantidad]
            print(plato)
            break
            # return render_template('consultarpla.html', plato=plato )
        
    return render_template('consultarpla.html', plato=plato)


@app.route('/VerPla', methods=['GET'])
def VerPla():
    # consultar platos
    print("hola")
    plato = []
    platos = platosasi1
    return render_template('consultarpla.html', platos=platos, plato=plato)


@app.route('/Agregapla', methods=['GET', 'POST'])
def agregapla():
    # agregar platos

    nombreplato = request.args.get('Nombre')
    precioplato = request.args.get('Precio')
    descripcionplato = request.args.get('Descripcion')
    cantidadplato = request.args.get('Cantidad')
    nuevoplato = [nombreplato, precioplato, descripcionplato, cantidadplato]
    platosasi1.append(nuevoplato)
    platos = platosasi1
    return render_template('agregarpla.html', platos=platos)


@app.route('/Eliminapla', methods=['GET', 'POST'])
def Elimipla():
    # eliminar platos
    nombreplato = request.args.get('Nombre')
    for i in range(len(platosasi1)):
        if nombreplato == platosasi1[i][0]:
            del platosasi1[i]
            break
        else:
            pass
    plato = platosasi1
    return render_template('eliminarpla.html', plato=plato)


if __name__ == '__main__':
    app.run(debug=True, port=5500)
