import json

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


##Cargamos el archivo JSON
with open(path+r"\json\\"+files["contacted_domains"]) as json_file:
  jj = json.load(json_file)