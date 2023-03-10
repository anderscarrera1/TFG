import bcrypt
import pymongo
import json
from pymongo import MongoClient


##Conexión con la base de datos.
cluster= MongoClient("mongodb+srv://admin:admin@cluster0.zme3x0y.mongodb.net/?retryWrites=true&w=majority")
db = cluster["VirusTotal_DB"]

##Conexión con la colección que tiene los archivos JSON.
collection = db["JSON_Files"]

##Conexión con la colección que tiene usuarios analistas.
user_analyst = db["user_analyst"]

##Conexión con la colección que tiene los usuarios json.
user_admin = db["user_admin"]

##Conexión con la colección de datos.
data = db["data"]

#################################################################################################################################################################################################################
##########                                                                ARCHIVOS Y EJEMPLOS                                                                            ########################################
#################################################################################################################################################################################################################


##JSON para subir a la colección de datos.
files = {
    "basic":"011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69.json",
    "behaviour":"011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_behaviour.json",
    "contacted_domains":"011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_contacted_domains.json",
    "contacted_ips":"011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_contacted_ips.json",
    "contacted_urls":"011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_contacted_urls.json",

    "dropped_files": "011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_dropped_files.json",
    "embedded_domains": "011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_embedded_domains.json",
    "embedded_ips": "011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_embedded_ips.json",
    "embedded_urls": "011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_embedded_urls.json",
    "similar_files": "011c24bce46c2ded7236482e0e36530dd27c937e31a0896e91659d9acd7ceb69_similar_files.json"}

##JSON de ejemplo
user1={"nombre":"juanma",
        "apellido":"gutierrez"}

user2={"nombre":"bicho",
        "apellido":"el rex",
        "popular_threat_name": [{"count": 6, "value": "razy"}, {"count": 2, "value": "harharminer"}]}

sampleList=[user1,user2]

def test():
    ##Insertar un elemento
    collection.insert_one(user2)

    ##Buscar elemento por campo
    res=collection.find({"nombre":"juanma"})
    for elem in res:
        print(elem)

    ##Imprimimos solo el campo que queremos
    for elem in res:
        print(elem["name"])

    ##Buscar TODOS los elementos
    res=collection.find({})
    for elem in res:
        print(elem)

    print("Done")

#################################################################################################################################################################################################################
##########                                                                COLECCION JSON                                                                                 ########################################
#################################################################################################################################################################################################################

##Borra todos los archivos de la colección de JSON.
def deleteAll():
    collection.delete_many({})


##Inserta una lista en la colección de JSON.
def insertAll(list):
    collection.insert_many(list)


##Inserta un elemento en la colección de JSON.
def insertOne(elem,name=""):
    elem["_id"]=name

    ##Guardar el tipo de cada arvchivo aumentará la velocidad a la hora de hacer transformaciones por lotes, ya que solo se buscarán los de ese tipo
    aux=name[64:].replace(".json","")
    if aux=="":
        aux="basic"
    else:
        aux=aux[1:]

    elem["type"]=aux
    collection.insert_one(elem)


##Recupera todos los elementos de la colección de JSON.
def retrieveAll():
    return collection.find({})


##Recupera todos los nombres de los elementos de la colección de JSON. Aumenta la velocidad a la hora de mostrar los archivos subidos
def retrieveAllNames():
    return collection.find({},{"_id":True})


##Recupera un elemento de la colección de JSON.
def retrieveOne(filename):
    res=collection.find({"_id":filename},{'_id': False,'type':False})
    for elem in res:
        return elem
    

##Recupera todos los elementos de la colección de JSON con el tipo indicado.
def retrieveByType(type):
    return collection.find({"type":type})


#################################################################################################################################################################################################################
##########                                                                COLECCION USUARIOS                                                                             ########################################
#################################################################################################################################################################################################################

##Borra todos los archivos de la colección de administrador.
def deleteAllAdmin():
    user_admin.delete_many({})


##Añadir un administrador
def addAdmin(username,password,name="",surname="",email=""):

    ##ENCRIPTAR DE ALGUNA FORMA

    ##passw = password.encode('utf-8')
    ##passw = bcrypt.hashpw(passw, bcrypt.gensalt(10))

    ##passw=hash(password)

    admin={"_id":username,
           "username":username,
           "password":password,
           "name":name,
           "surname":surname,
           "email":email}
    user_admin.insert_one(admin)


##Añadir un administrador
def updateAdmin(username,password,name="",surname="",email=""):
       
    admin={"_id":username,
        "username":username,
        "password":password,
        "name":name,
        "surname":surname,
        "email":email}
    
    user_admin.update_one({"_id":username},{"$set":admin})


##Comprobar si el administrador está en la base de datos
def checkAdminLogin(username,password):
    ##Buscar elemento por campo
    res=user_admin.find({"username":username})
    res=list(res)

    if len(res)==0:
        ##print("El usuario no existe")
        return False
    else:
        if res[0]["password"] != password:

            ##print("Contraseña incorrecta")
            return False
        else:
            ##print("OK")
            return True


##Recupera todos los elementos de la colección de admin.
def retrieveAllAdmin():
    return user_admin.find({},{"_id":False})


##Borra el administrador que recibe como parámetro
def deleteAdmin(id):
    user_admin.delete_one({"_id":id})





##Comprobar si el analista está en la base de datos.
def checkAnalystLogin(username,password):
    ##Buscar elemento por campo
    res=user_analyst.find({"username":username})
    res=list(res)

    if len(res)==0:
        ##print("El usuario no existe")
        return False
    else:
        if res[0]["password"] != password:

            ##print("Contraseña incorrecta")
            return False
        else:
            ##print("OK")
            return True


##Borra todos los archivos de la colección de analista.
def deleteAllAnalyst():
    user_analyst.delete_many({})


##Añadir un analista
def addAnalyst(username,password,name="",surname="",email=""):

    ##ENCRIPTAR DE ALGUNA FORMA

    ##passw = password.encode('utf-8')
    ##passw = bcrypt.hashpw(passw, bcrypt.gensalt(10))

    ##passw=hash(password)

    analyst={"_id":username,
           "username":username,
           "password":password,
           "name":name,
           "surname":surname,
           "email":email}
    user_analyst.insert_one(analyst)


##Recupera todos los elementos de la colección de analista.
def retrieveAllAnalyst():
    return user_analyst.find({},{"_id":False})


##Borra el analista que recibe como parámetro
def deleteAnalyst(id):
    user_analyst.delete_one({"_id":id})


##Añadir un analista
def updateAnalyst(username,password,name="",surname="",email=""):
       
    analyst={"_id":username,
        "username":username,
        "password":password,
        "name":name,
        "surname":surname,
        "email":email}
    
    user_analyst.update_one({"_id":username},{"$set":analyst})


#################################################################################################################################################################################################################
##########                                                                COLECCION DE DATOS                                                                             ########################################
#################################################################################################################################################################################################################

##Sube a la base de datos los 10 archivos tipo para la conversion por lotes
def uploadData():
    path = r"C:\Users\xhola\OneDrive\Escritorio\wannacry\dataset_wannacry\dataset_wannacry_json\\"

    for elem in files:
        with open(path+files[elem]) as data_file:    
            d=json.load(data_file) 

        d["_id"]=elem
        data.insert_one(d)
    print("done")


##Recupera todos los elementos de la colección de datos.
def retrieveAllData():
    return data.find({})


##Recupera un elemento de la colección de datos.
def retrieveOneData(filename):
    res=data.find({"_id":filename},{'_id': False})
    for elem in res:
        return elem

##uploadData()

##deleteAllAnalyst()
##addAnalyst("test", "test")

##checkAdminLogin("admin","admin")
##deleteAllAdmin()
##addAdmin("admin", "admin")

##test()
##deleteAll()
##insertAll(sampleList)