import csv
import json
import os
import glob
import shutil

import numpy as np
import pandas as pd
import pathlib

from python_files import DBModule


##Función que borra todos los archivos subidos a la aplicación.
def deleteFiles(path):

    jsonPath=path+r"\json"
    csvPath=path+r"\csv"

    """##Se borran los elementos de la carpeta de JSON.
    for elem in os.listdir(jsonPath):
        if elem.endswith('.json'):
          os.remove(jsonPath+"\\"+elem)"""

    ##Se borran los CSV de la carpeta de CSV.
    for elem in os.listdir(csvPath):
        if elem.endswith('.csv'):
          os.remove(csvPath+"\\"+elem)

    ##Se borran las carpetas de la carpeta de CSV.
    for elem in os.listdir(csvPath):
          shutil.rmtree(csvPath+"\\"+elem)


##Función que convierte un archivo JSON a CSV aplanando todos sus campos.
def toCSV(jsonFile, name=''):

    ##Listas para devolver el resultado.
    rows = []
    columns = []

    ##Función para aplanar el json.
    def flatten(jsonFile, name):
       for elem in jsonFile:
        
        ##Si es el elemento es un diccionario, se vuelve a llamar a la función aplanando su nombre.
        if type(jsonFile[elem]) is dict:
          flatten(jsonFile[elem],name+elem+".")

        ##Si el elemento es una lista, se itera sobre sus elementos.
        elif type(jsonFile[elem]) is list:
          cont=0

          for e in jsonFile[elem]:

            ##Si es el elemento es un diccionario, se vuelve a llamar a la función aplanando su nombre.
            if type(e) is dict:
              flatten(e,name+elem+str(cont)+".")

            ##Si el elemento es un valor, se añade al resultado.  
            else:            
              if elem != "_id":
                columns.append(name+elem+str(cont))
                rows.append(e)
              
            cont+=1

        ##Si el elemento es un valor, se añade al resultado.  
        else:
          if elem != "_id":
            columns.append(name+elem)
            rows.append(jsonFile[elem])
       
       return {"rows":rows,"columns":columns}
        
    res = flatten(jsonFile,name)

    return res


##Función que convierte un archivo JSON a CSV aplanando todos sus campos en función de las etiquetas seleccionadas.
def toCSVByTags(jsonFile, filename, tags, path,name=''):

    ##Listas para devolver el resultado.
    rows = []
    columns = []
    tags = tags
    ##Función para aplanar el json.
    def flattenByTags(jsonFile, name):
       for elem in jsonFile:

        ##El aplanado solo se le aplica a los elementos seleccionados mediante las etiquetas.
        if elem in tags:
          
          ##Si es el elemento es un diccionario, se vuelve a llamar a la función aplanando su nombre.
          if type(jsonFile[elem]) is dict:
            flattenByTags(jsonFile[elem],name+elem+".")

          ##Si el elemento es una lista, se itera sobre sus elementos.
          elif type(jsonFile[elem]) is list:
            cont=0

            for e in jsonFile[elem]:

              ##Si es el elemento es un diccionario, se vuelve a llamar a la función aplanando su nombre.
              if type(e) is dict:
                flattenByTags(e,name+elem+str(cont)+".")
              
              ##Si el elemento es un valor, se añade al resultado
              else:
                columns.append(name+elem+str(cont))
                rows.append(e)
                
              cont+=1

          ##Si el elemento es un valor, se añade al resultado
          else:
            columns.append(name+elem)
            rows.append(jsonFile[elem])

       return {"rows":rows,"columns":columns}   

    fjson = flattenByTags(jsonFile,name) 
  
    ##Se crea un directorio con el nombre del archivo en caso de que no exista.
    if not os.path.exists(path+r"\csv\\"+filename[0:64]):
        os.makedirs(path+r"\csv\\"+filename[0:64])

    ##Directorio donde se va a guardar el elemento.
    currentPath=path+r"\csv\\"+filename[0:64]+"\\"+filename.replace(".json", "")+".csv"

    ##Se crea al writer y se guardan los elementos aplanados como CSV.
    with open(currentPath, 'w',encoding="utf-8") as f:
      write = csv.writer(f)
      
      write.writerow(fjson["columns"])
      write.writerow(fjson["rows"])

    return fjson


##Función que obtiene los archivos json o csv de un directorio.
def listDirectory(path):
    res = []

    ##Por cada elemento del csv, se añaden los que sean JSON o CSV.
    for elem in os.listdir(path):

        if elem.endswith('.csv'):
            res.append(elem)

        if elem.endswith('.json'):
            res.append(elem)

    return res


##Función que lee un directorio y devuelve una lista de listas con los archivos y otra con el nombre en comun de esos los archivos pertenecientes a la sublista.
def listDirectoryGroup():
    titles = []
    aux=[]
    files = []

    ##Se obtienen los elementos de la base de datos.
    BDObjects=DBModule.retrieveAllNames()

    ##Se añaden los elementos a una lista auxiliar y los titulos a la lista de titulos.
    for elem in BDObjects:
      if elem["_id"].endswith('.json'):

        if not any(elem["_id"][0:10] in l for l 
        in titles):

          ##Se añaden los titulos a la lista de titulos.
          titles.append(elem["_id"][0:64])

        ##Se añaden todos los archivos a la lista auxiliar.
        aux.append(elem["_id"])

    ##Se añaden a la lista de archivos las sublistas que corresponden con los titulos.
    for elem["_id"] in titles:
      matches = [l for l in aux 
      if elem["_id"] in l]

      files.append(matches)

    return {"titles":titles, "files":files}


##Función que transforma todos los archivos json de un directorio a csv.
def transformAll(path):
    
    res= DBModule.retrieveAll()
    
    ##Se itera sobre cada elemento del directorio.
    for elem in res:
      fjson=toCSV(elem)

      ##Se crea un directorio con el nombre del archivo en caso de que no exista.
      if not os.path.exists(path+r"\csv\\"+elem["_id"][0:64]):
         os.makedirs(path+r"\csv\\"+elem["_id"][0:64])

      ##Directorio donde se va a guardar el elemento.
      currentPath=path+r"\csv\\"+elem["_id"][0:64]+"\\"+elem["_id"].replace(".json", "")+".csv"

      ##Se crea al writer y se guardan los elementos aplanados como CSV.
      with open(currentPath, 'w',encoding="utf-8") as f:
        write = csv.writer(f)
        
        write.writerow(fjson["columns"])
        write.writerow(fjson["rows"])


##Función que transforma los archivos de un lote a csv.
def transformBatch(type,tags,path):    
    res= DBModule.retrieveByType(type)
    
    ##Se itera sobre cada elemento del directorio y se le aplica la función toCSVByTags.
    for elem in res:
      toCSVByTags(elem,elem["_id"],tags,path)

