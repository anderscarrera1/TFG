import jinja2
from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

import os
import json
from python_files import utilities
from python_files import convertor

#################################################################################################################################################################################################################
##########                                                                 PARÁMETROS FLASK                                                                                   ###################################
#################################################################################################################################################################################################################
app = Flask(__name__)

path=r'app_project\uploaded_files'
path = os.getcwd()+r"\uploaded_files"
app.config['UPLOAD_FOLDER']= path+"\\json\\"


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
##Página principal.
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/examine/")
def examine():
    return render_template("examine.html")


##Función para subir los archivos y pasar a la siguiente página.
@app.route("/upload/", methods=["POST"])
def upload():
    if request.method == "POST":
  
        files = request.files.getlist("file")
        if files[0].filename:
            for file in files:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
                        
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

    return redirect("/uploadedFiles/")


##Página que muestra cada uno de los archivos subidos.
@app.route("/uploadedFiles/<path:filename>",methods = ["POST", "GET"])
def log(filename):
    
    with open(path+r"\json\\"+filename) as data_file:    
        jsonFile=json.load(data_file) 
    
    if request.method=="POST":
        tags=request.form.getlist("example")
        convertor.toCSVByTags(jsonFile, filename,tags,path)


    return render_template("file.html",name=filename,jsonFile=jsonFile)
    

##Función principal.
if __name__ == "__main__":
    app.run()
