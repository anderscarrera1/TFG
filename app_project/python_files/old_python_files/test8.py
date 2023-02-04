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


def fflatten(jsonFile, tags, name=''):
    rows = []
    columns = []
    tags = tags
    def flatten(jsonFile, name):
       for elem in jsonFile:
        
        if elem in tags:
          ##print(elem)
          if type(jsonFile[elem]) is dict:
            flatten(jsonFile[elem],name+elem+".")

          elif type(jsonFile[elem]) is list:
            cont=0

            for e in jsonFile[elem]:
              if type(e) is dict:
                flatten(e,name+elem+str(cont)+".")
                
              else:
                ##print("   "+name+elem+str(cont),":",e)

                columns.append(name+elem+str(cont))
                rows.append(e)
                
              cont+=1

          else:
            ##print(name+elem, ":" ,jsonFile[elem]) 

            columns.append(name+elem)
            rows.append(jsonFile[elem])

       return {"rows":rows,"columns":columns}
          


    res = flatten(jsonFile,name)

    return res



##Cargamos el archivo JSON
with open(path+r"\json\\"+files["embedded_domains"]) as json_file:
  jsonFile = json.load(json_file)


##Aplanamos el arvhivo JSON
res=fflatten(jsonFile)

##Guardamos el archivo JSON como CSV
"""with open(path+r"\csv\\"+files["basic"]+".csv", 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    
    aux=[]
    for elem in res["columns"]:
        
        x=elem.replace('>','_')
        aux.append(x) 

    write.writerow(aux)
    write.writerow(res["rows"])
  
printTags(res["columns"],res["columns"][0])"""

for elem in res["rows"]:
  print(elem)


##df.to_csv(path+r"\csv\\"+files["basic"]+".csv", sep=",")