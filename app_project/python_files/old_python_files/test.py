import formatConvertor
import pandas as pd
import json
import csv
import os

from flatten_json import flatten

##formatConvertor.readFile()

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



def test():
    with open (path+r"\json\\"+name, "r") as f:
        data = json.load(f)
        names = data["data"]

    with open (path+r"\csv\\"+name+".csv", "w") as f:
        fieldnames = names[0].keys()
        writer = csv.dictwriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for name in names:
            writer.writerow(name)

def pprintJson(path, name):
    with open(path+r"\json\\"+name) as data_file:    
        d=json.load(data_file) 

    df2 = json.dumps(d, indent=2)
    print(df2)


def pprintJson2(path, name):
    with open(path+r"\json\\"+name) as data_file:    
        d=json.load(data_file) 

    fjson = flatten(d)

    x=pd.json_normalize(d)
    print(x)

    fjson.to_csv(path+r"\csv\\"+name+".csv", sep=",")
    ##data_file = open(path+r"\csv\\"+name+".csv", 'w', newline='')
    ##csv_writer = csv.writer(data_file)



pprintJson2(path,files["basic"])

