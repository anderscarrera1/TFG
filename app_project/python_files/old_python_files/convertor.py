import csv
import json
import os
import glob

import numpy as np
import pandas as pd
import pathlib


##Función que borra todos los archivos subidos a la aplicación.
def deleteFiles(path):

    jsonPath=path+r"\json"
    csvPath=path+r"\csv"

    ##Se borran los elementos de la carpeta de JSON.
    for elem in os.listdir(jsonPath):
        if elem.endswith('.json'):
          os.remove(jsonPath+"\\"+elem)

    ##Se borran los elementos de la carpeta de CSV.
    for elem in os.listdir(csvPath):
        if elem.endswith('.csv'):
          os.remove(csvPath+"\\"+elem)


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
              columns.append(name+elem+str(cont))
              rows.append(e)
              
            cont+=1

        ##Si el elemento es un valor, se añade al resultado.  
        else:

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
    
    ##Se abre un writer y se guarda el archivo aplanado como csv.
    with open(path+r"\csv\\"+filename.replace(".json", "")+".csv", 'w',encoding="utf-8") as f:
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
def listDirectoryGroup(path):
    titles = []
    aux=[]
    files = []

    ##Se añaden los elementos a una lista auxiliar y los titulos a la lista de titulos.
    for elem in os.listdir(path):
      if elem.endswith('.json'):

        if not any(elem[0:10] in l for l 
        in titles):

          ##Se añaden los titulos a la lista de titulos.
          titles.append(elem[0:64])

        ##Se añaden todos los archivos a la lista auxiliar.
        aux.append(elem)

    ##Se añaden a la lista de archivos las sublistas que corresponden con los titulos.
    for elem in titles:
      matches = [l for l in aux 
      if elem in l]

      files.append(matches)

    return {"titles":titles, "files":files}


##Función que transforma todos los archivos json de un directorio a csv.
def transformAll(path):
    
    ##Llamada a la función "listDirectory()" para obtener los elementos del directorio.
    res=listDirectory(path+"\json")
    
    ##Se itera sobre cada elemento del directorio.
    for elem in res:

      ##Se abre el el primer archivo como json y se aplana con la función "toCSV()".
      with open(path+r"\json\\"+elem) as json_file:
        j= json.load(json_file)

      fjson=toCSV(j)

      ##se crea al writer y se guardan los elementos aplanados como CSV.
      
      with open(path+r"\csv\\"+elem.replace(".json", "")+".csv", 'w',encoding="utf-8") as f:
        write = csv.writer(f)
        
        write.writerow(fjson["columns"])
        write.writerow(fjson["rows"])
