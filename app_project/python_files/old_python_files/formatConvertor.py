import csv
import json
import os
import glob

import numpy as np
import pandas as pd
import pathlib

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def listDirectory(path):
    res = []

    for p in os.listdir(path):

        if p.endswith('.csv'):
            res.append(p)

        if p.endswith('.json'):
            res.append(p)

    print(" > Los archivos que se encuentran en el directorio son los siguientes: \n")
    print("  "+bcolors.OKGREEN,res,bcolors.ENDC)

    return res




def csvToJson(path,csvName,jsonName):

  print(" > Convirtiendo CSV a JSON...\n")

  df = pd.read_csv(path+csvName,index_col=False)
  df.to_json(path+jsonName)

  print(" > Se ha creado con éxito el archivo JSON:"+bcolors.OKGREEN, jsonName+ bcolors.ENDC,"\n")

  return df

def jsonToCsv(path,csvName,jsonName):

  print(" > Convirtiendo JSON a CSV...\n")

  df = pd.read_json(path+jsonName)
  df.to_csv(path+csvName, index=False)

  print(" > Se ha creado con éxito el archivo CSV:"+bcolors.OKGREEN, csvName+ bcolors.ENDC,"\n")

def readFile():
    print("\n > Introduzca el directorio donde se encuentran los archivos a convertir: \n")
    path = input()
    path = "C:\\Users\\A\\Desktop\\python\\csv y json\\"

    print("\n")
    l=listDirectory(path)
    
    x=True
    while x==True:

        print("\n > Seleccione el archivo que quiere convertir: \n")
        chosenFile = input()
        print("\n > Se ha seleccionado:" +bcolors.OKGREEN, chosenFile+ bcolors.ENDC,"\n")

        extension=pathlib.Path(path+chosenFile).suffix
        resultFile= chosenFile.replace(extension,"")


        if chosenFile=="0":
            print(" > Mostrando de nuevo el directorio... \n")
            listDirectory(path)
            x=True

        elif chosenFile not in l:
            print(" > "+bcolors.WARNING+"Ese archivo no es válido. Por favor introduzca otro nombre o 0 para volver a ver los archivos disponibles."+bcolors.ENDC)
            x=True

        elif extension== ".csv":
            csvToJson(path,chosenFile,resultFile+".json")
            x=False

        elif extension== ".json":
            jsonToCsv(path,resultFile+".csv",chosenFile)
            x=False