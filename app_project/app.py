import jinja2
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError

import os
import json
from datetime import timedelta
from python_files import utilities
from python_files import convertor
from python_files import DBModule
 

#################################################################################################################################################################################################################
##########                                                                 PARÁMETROS FLASK                                                                                   ###################################
#################################################################################################################################################################################################################
app = Flask(__name__,static_folder=r'templates\images')

path=r'app_project\uploaded_files'
app.config['UPLOAD_FOLDER']= path+"\\json\\"
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(days=7)
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)



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

#################################################################    PÁGINAS Y FUNCIONES GENERALES    ###########################################################################################################

##Página para hacer el login.
@app.route("/")
def login():
   if "username" in session:
        if session["type"]=="admin":
            return redirect("/indexAdmin")
        else:
            return redirect("/indexAnalyst")
   else:
        return render_template("login.html")


##Función para hacer logout
@app.route("/logout", methods=["POST","GET"])
def logout():
    session.pop("username",None)
    return redirect("/")


#################################################################    PÁGINAS Y FUNCIONES ANALISTA    ###########################################################################################################

##Login analista *TESTEAR QUE FUNCIONA CON UNA CUENTA DE ANALISTA*
@app.route("/loginAnalyst", methods=["POST","GET"])
def loginAnalyst():
    if request.method=="POST":
        
        username = request.form["username"]
        password = request.form["password"]
        permanent = request.form.get("permanent")

        if DBModule.checkAnalystLogin(username,password):
            session["username"]=username
            session["type"] = "analyst"

            if permanent == "permanent":
                session.permanent=True
            else:
                session.permanent=False
                
            return redirect("/indexAnalyst")
        
        else:
            flash("Wrong username or password.","error")
            return redirect("/")
    else:
        if "username" in session:
            return redirect("/indexAnalyst")
        return redirect("/")


##Página principal analista
@app.route("/indexAnalyst")
def homeAnalyst():
    if "username" in session:
        username = session["username"]
        return render_template("analyst_index.html", username=username)
    else:
        return redirect("/")


##Página del analista que muestra una lista con todos los archivos subidos
@app.route("/uploadedFilesAnalyst")
def uploadedFilesAnalyst():
    names2= convertor.listDirectoryGroup()
  
    return render_template("analyst_uploads.html", files=names2["titles"], files2=names2["files"])


##Páginas del analista que muestran cada uno de los archivos subidos. También se encarga de transformar los archivos a csv mediante selección de etiquetas.
@app.route("/uploadedFilesAnalyst/<path:filename>",methods = ["POST", "GET"])
def logAnalyst(filename):
    
    jsonFile = DBModule.retrieveOne(filename)
    
    if request.method=="POST":
        tags=request.form.getlist("example")
        flash("File converted to CSV succesfully!")
        convertor.toCSVByTags(jsonFile, filename,tags,path)

    return render_template("analyst_file.html",name=filename,jsonFile=jsonFile)


##Página del analista para transformar archivos por lote
@app.route("/batchesAnalyst")
def batches():

    data=DBModule.retrieveAllData()
    aux=[]
    for elem in data:
        aux.append(elem["_id"])

    return render_template("analyst_batch.html",data=aux)


##Páginas del analista que muestran cada uno de los archivos subidos. También se encarga de transformar los archivos a csv mediante selección de etiquetas.
@app.route("/batchesAnalyst/<path:filename>",methods = ["POST", "GET"])
def logBatchAnalyst(filename):
    
    jsonFile = DBModule.retrieveOneData(filename)

    if request.method=="POST":
        tags=request.form.getlist("example")
        convertor.transformBatch(filename,tags,path)
        flash("All "+filename+ " files converted to CSV succesfully!")

    return render_template("analyst_batch_file.html",name=filename,jsonFile=jsonFile)


##Función del analista que transforma todos los archivos subidos a csv.
@app.route("/convert/", methods = ["POST"])
def convertAnalyst():
    flash("All files converted to CSV succesfully!")
    convertor.transformAll(path)
    
    return redirect("/uploadedFilesAnalyst")


#################################################################    PÁGINAS Y FUNCIONES ADMINISTRADOR    ###########################################################################################################

##Página de login administrador
@app.route("/loginAdmin", methods=["POST","GET"])
def loginAdmin():
    if request.method=="POST":
        
        username = request.form["username"]
        password = request.form["password"]
        permanent = request.form.get("permanent")

        if DBModule.checkAdminLogin(username,password):
            session["username"]=username
            session["type"] = "admin"

            if permanent == "permanent":
                session.permanent=True
            else:
                session.permanent=False

            return redirect("/indexAdmin")
        
        else:
            flash("Wrong username or password.","error")
            return redirect("/")
    else:
        if "username" in session:
            return redirect("/indexAdmin")
        return redirect("/")


##Página principal administrador
@app.route("/indexAdmin")
def homeAdmin():
    if "username" in session:
        username = session["username"]
        return render_template("admin_index.html", username=username)
    else:
        return redirect("/")


##Página del administrador para examinar archivos
@app.route("/examineAdmin")
def examine():
    return render_template("admin_examine.html")


##Página del administrador que muestra una lista con todos los archivos subidos
@app.route("/uploadedFilesAdmin")
def uploadedFilesAdmin():
    names2= convertor.listDirectoryGroup()
  
    return render_template("admin_uploads.html", files=names2["titles"], files2=names2["files"])


##Páginas del administrador que muestran cada uno de los archivos subidos. También se encarga de transformar los archivos a csv mediante selección de etiquetas.
@app.route("/uploadedFilesAdmin/<path:filename>", methods = ["POST", "GET"])
def logAdmin(filename):
    
    jsonFile = DBModule.retrieveOne(filename)
    
    if request.method=="POST":
        tags=request.form.getlist("example")
        convertor.toCSVByTags(jsonFile, filename,tags,path)

    return render_template("admin_file.html",name=filename,jsonFile=jsonFile)


##Página del administrador para examinar archivos
@app.route("/manageAccountsAdmin")
def manageAccounts():
    admin=DBModule.retrieveAllAdmin()
    adminList=[]
    adminNameList=[]
    for elem in admin:
        adminList.append(elem)
        adminNameList.append(elem["username"])

    analyst=DBModule.retrieveAllAnalyst()
    analystList=[]
    analystNameList=[]
    for elem in analyst:
        analystList.append(elem)
        analystNameList.append(elem["username"])

    return render_template("admin_manage.html",admin=adminList,adminNames=adminNameList,analyst=analystList,analystNames=analystNameList)


##Función del administrador para subir los archivos y pasar a la siguiente página.
@app.route("/uploadAdmin", methods=["POST","GET"])
def uploadAdmin():
    if request.method == "POST":
  
        files = request.files.getlist("file")
        print(len(files))
        if files[0].filename:     
            
            for file in files:
                aux=json.load(file)
                DBModule.insertOne(aux,file.filename)

            flash("All files uploaded succesfully!")                       
            return redirect("/uploadedFilesAdmin")
        else:
            
            return redirect("/examine")


##Función del administrador que borra todos los archivos subidos a la aplicación.
@app.route("/delete", methods = ["POST"])
def deleteAdmin():
    convertor.deleteFiles(path)
    DBModule.deleteAll()
    flash("All files deleted succesfully!")
    return redirect("/uploadedFilesAdmin")


##Función del administrador para añadir una nueva cuenta.
@app.route("/newAccount/", methods = ["POST"])
def newAccount():
    username=request.form["username"]
    password=request.form["password"]
    name=request.form["name"]
    surname=request.form["surname"]
    email=request.form["email"]
    type = request.form.get("type")

    if type=="analyst":
        flash("Analyst created successfully!")
        DBModule.addAnalyst(username,password,name,surname,email)
    else:
        flash("Administrator created successfully!")
        DBModule.addAdmin(username,password,name,surname,email)

    return redirect("/manageAccountsAdmin")


##Función del administrador para borrar una cuenta
@app.route("/deleteAccount/", methods = ["POST"])
def deleteAccount():
    type = request.form.get("type")
    username = request.form.get("username")
    print(type)

    if type=="analyst":
        flash("Analyst deleted successfully!")
        DBModule.deleteAnalyst(username)
    else:
        flash("Administrator deleted successfully!")
        DBModule.deleteAdmin(username)

    return redirect("/manageAccountsAdmin")


##Función del administrador para actualizar la información de una cuenta.
@app.route("/updateAccount/", methods = ["POST"])
def updateAccount():
    username=request.form["username"]
    password=request.form["password"]
    name=request.form["name"]
    surname=request.form["surname"]
    email=request.form["email"]
    type = request.form.get("type")

    if type=="analyst":
        flash("Analyst updated successfully!")
        DBModule.updateAnalyst(username,password,name,surname,email)
    else:
        flash("Administrator updated successfully!")
        DBModule.updateAdmin(username,password,name,surname,email)

    return redirect("/manageAccountsAdmin")


####################################################################    FUNCIÓN PRINCIPAL    ##############################################################################################################

##Función principal.
if __name__ == "__main__":
    app.run()
    
