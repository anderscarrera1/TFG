import jinja2
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

import os
import json
from python_files import utilities
from python_files import convertor
from python_files import DBModule

#################################################################################################################################################################################################################
##########                                                                 PARÁMETROS FLASK                                                                                   ###################################
#################################################################################################################################################################################################################
app = Flask(__name__)

path=r'app_project\uploaded_files'
app.config['UPLOAD_FOLDER']= path+"\\json\\"
app.secret_key = "secret"


#################################################################################################################################################################################################################
##########                                                                      FILTROS                                                                                       ###################################
#################################################################################################################################################################################################################
@app.template_test("list")
def is_list(value):
    return isinstance(value, list)

##Filtro para comprarar si un elemento es un diccionario.
@app.template_test("dict")
def is_list(value):
    return isinstance(value, dict)

#################################################################################################################################################################################################################
##########                                                                PÁGINAS Y FUNCIONES                                                                                 ###################################
#################################################################################################################################################################################################################

##########                  GENERALES         ###############################################################################################################################

##Página para hacer el login.
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST","GET"])
def loginAnalyst():

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        print("Username:",username)
        print("Password:",password)
        session["username"]=username
        return redirect("/index")
    else:
        if "username" in session:
            return redirect("/index")
        return render_template("/")
    

@app.route("/login", methods=["POST","GET"])
def loginAdmin():
    username = request.form["username"]
    password = request.form["password"]
    print("Username:",username)
    print("Password:",password)
    return redirect("/index")


@app.route("/logout", methods=["POST","GET"])
def logout():
    session.pop("username",None)
    return redirect("/")


##Página principal.
@app.route("/index")
def home():
    if "username" in session:
        username = session["username"]
        return render_template("index.html", username=username)
    else:
        return redirect("/")

##Página para examinar archivos
@app.route("/examine/")
def examine():
    return render_template("examine.html")


##Función para subir los archivos y pasar a la siguiente página.
@app.route("/upload/", methods=["POST","GET"])
def upload():
    if request.method == "POST":
  
        files = request.files.getlist("file")
        if files[0].filename:     
            
            for file in files:
                aux=json.load(file)
                DBModule.insertOne(aux,file.filename)
                                        
            return redirect("/uploadedFiles/")
        else:
            
            return redirect("/examine/")


##Página que muestra todos los archivos subidos.
@app.route("/uploadedFiles/")
def uploadedFiles():
    names2= convertor.listDirectoryGroup(path+"\\json\\")
  
    return render_template("uploads.html", files=names2["titles"], files2=names2["files"])


##Función que transforma todos los archivos subidos a csv.
@app.route("/convert/", methods = ["POST"])
def convert():
    convertor.transformAll(path)

    return redirect("/uploadedFiles/")


##Función que borra todos los archivos subidos a la aplicación.
@app.route("/delete/", methods = ["POST"])
def delete():
    convertor.deleteFiles(path)
    DBModule.deleteAll()
    return redirect("/uploadedFiles/")


##Página que muestra cada uno de los archivos subidos.
@app.route("/uploadedFiles/<path:filename>",methods = ["POST", "GET"])
def log(filename):
    
    jsonFile = DBModule.retrieveOne(filename)
    
    if request.method=="POST":
        tags=request.form.getlist("example")
        convertor.toCSVByTags(jsonFile, filename,tags,path)

    return render_template("file.html",name=filename,jsonFile=jsonFile)

##Función principal.
if __name__ == "__main__":
    app.run()
