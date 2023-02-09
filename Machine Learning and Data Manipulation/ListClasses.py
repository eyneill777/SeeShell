import os
import json
import simplejson

with open("config.json", "r") as f:
    config = json.load(f)

path = config["rawDataPath"]

species = {}
genuses = {}

for filename in os.listdir(path):
    s = filename.split("_")
    binome = s[0]+" "+s[1]
    genus = s[0]
    
    
    if binome not in species:
        species[binome] = 1
    else:
        species[binome] = species[binome]+1
        
    if genus not in genuses:
        genuses[genus] = 1
    else:
        genuses[genus] = genuses[genus]+1

        
        
with open("species.json", "w") as f:
    f.write(simplejson.dumps(simplejson.loads(json.dumps(species)), indent=4, sort_keys=True))
    f.close()
    
with open("genuses.json", "w") as f:
    f.write(simplejson.dumps(simplejson.loads(json.dumps(genuses)), indent=4, sort_keys=True))
    f.close()
    
print(str(len(species))+" distinct species")
print(str(len(genuses))+" distinct genuses")