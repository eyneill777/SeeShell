import os
import shutil
import json

"""
Copy image dataset into a format which is easily imported into tensorflow
"""

with open("config.json", "r") as f:
    config = json.load(f)

inputPath = config["rawDataPath"]
genusPath = config["genusPath"]
speciesPath = config["speciesPath"]

#create output folders if they don't exist
if not os.path.exists(genusPath):
    os.makedirs(genusPath)
if not os.path.exists(speciesPath):
    os.makedirs(speciesPath)

count = 0
#iterate over input files and copy them to the relevant locations
for filename in os.listdir(inputPath):
    s = filename.split("_")
    binome = s[0]
    if s[1]:
        binome = binome+" "+s[1]
    genus = s[0]
    
    gp = os.path.join(genusPath, genus)
    sp = os.path.join(speciesPath, binome)
    
    if not os.path.exists(gp):
        os.makedirs(gp)
    if not os.path.exists(sp):
        os.makedirs(sp)
    
    shutil.copy(os.path.join(inputPath, filename), gp)
    shutil.copy(os.path.join(inputPath, filename), sp)
    
    if count%1000 == 0:
        print(count)
    count = count+1