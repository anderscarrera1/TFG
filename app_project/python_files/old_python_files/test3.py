import json
import csv
import pprint
import pandas as pd
from flatten_json import flatten


path=r'app_project\uploaded_files'

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



##nested_json = nested_json["_via_img_metadata"]


def fflatten(x, name=''):
    rows = []
    columns = []
    aux = []
    def flatten(x, name):
        
        ##Si el elemento es un diccionario:
        if type(x) is dict:

            ##Iteramos cada elemento del diccionario.
            for a in x:

                ##Concatenamos el nombre a la columna del csv y volvemos a pasar todo a la función.
                ## -Si el elemento del diccionario vuelve a ser un diccionario, volvemos a hacer lo mismo.
                ## -Si el elemento del diccionario es simplemente un campo, lo añadimos a la fila.
                flatten(x[a], name + a + '>')

        ##Si el elemento es una lista:
        elif type(x) is list:

            ##Con un contador diferenciaremos cada uno de los elementos de la lista
            i = 0

            ##Ieramos cada elemento de la lista
            for a in x:

                ##Concatenamos el nombre a la columna del csv y volvemos a pasar todo a la función.
                ## -Si el elemento de la lista vuelve a ser una lista, volvemos a hacer lo mismo.
                ## -Si el elemento de la lista es simplemente un campo, lo añadimos a la fila.
                flatten(a, name + str(i) + '>')
                i += 1
        else:

            ##Añadimos el elemento al diccionario.
            rows.append(x)

            ##Eliminamos la ultima "_" con [:-1]
            columns.append(name[:-1])

        return {"rows":rows,"columns":columns}

    res = flatten(x,name)

    return res


def printTags(columns, elem, inden=""):
    
    ##Aqui esta el fallo
    l=elem.split(">",1)[0]

    
    if len(columns[0])!=0:  

         ##Imprimimos el primer elemento de la lista.
        print(inden+l)

        aux=[]

        ##Hacemos una lista con todos los elementos que comienzan por el que hemos impreso.
        for x in columns:
            if l in x:
                length = len(l)+1
                sus=x[length:]

                ##Seguramente haya que cambiar esto y sacarlo del if.
                aux.append(sus)  
                columns=aux
                ##print("-Primer elemento: ",x)
                printTags(columns,sus, inden+"  ")
        else:
            if("" in columns):
                columns = columns.remove("")
       
            

    ##printTags(columns, l[0], inden+">")


##Cargamos el archivo JSON
with open(path+r"\json\\"+files["basic"]) as json_file:
  nested_json = json.load(json_file)


##Aplanamos el arvhivo JSON
res=fflatten(nested_json)
df = pd.Series(res).to_frame()

##Guardamos el archivo JSON como CSV
with open(path+r"\csv\\"+files["basic"]+".csv", 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    
    aux=[]
    for elem in res["columns"]:
        
        x=elem.replace('>','_')
        aux.append(x) 

    write.writerow(aux)
    write.writerow(res["rows"])
  
printTags(res["columns"],res["columns"][0])

##df.to_csv(path+r"\csv\\"+files["basic"]+".csv", sep=",")