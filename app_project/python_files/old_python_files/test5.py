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



j={
"country abbreviation": "US",
"places": [
    {
        "place name": "Belmont",
        "longitude": "-71.4594",
        "post code": "02178",
        "latitude": "42.4464"
    },
    {
        "place name": "Belmont",
        "longitude": "-71.2044",
        "post code": "02478",
        "latitude": "42.4128"
    }
],
"country": "United States",
"place name": "Belmont",
"state": "Massachusetts",
"state abbreviation": "MA"
}

"""for elem in j:
    
    if elem=="places":
        for place in j["places"]:
            for data in place:
                print("     ",data, ":",place[data])
    else:
        print(elem, ":",j[elem])"""


##Cargamos el archivo JSON
with open(path+r"\json\\"+files["contacted_domains"]) as json_file:
  jj = json.load(json_file)

print("\n")
for elem in jj:
    print(elem)
    if(elem=="meta"):
        for mt in jj[elem]:
            print("  ",mt,":",jj[elem][mt])

    if(elem=="data"):
        for dt in jj[elem]:
            for x in dt:
                print("  ",x)
                
                if(x=="type"):
                    for mt in jj[elem]:
                        print("  ",mt,":",jj[elem][mt])

    if(elem=="links"):
        for lk in jj[elem]:
            print("  ",lk,":",jj[elem][lk])

print("\n")
