import time
import sys
import os
import json
import tensorflow as tf
from ibm_watson_machine_learning import APIClient

with open("config.json", "r") as f:
    config = json.load(f)
    watsonConfig = config["watson"]

class FileDropService:
    
    def __init__(self):
        self.statuses = {}
        
        try:
            while True:
                for filename in os.listdir(config["dropFolder"]):
                    splitName = filename.split('.')
                    if filename not in config["ignoredFiles"] and splitName[len(splitName)-1] in config["approvedFileTypes"]: 
                        filepath = os.path.join(config["dropFolder"], filename)
                        if os.path.isfile(filepath):
                            self.processFile(filepath)

                time.sleep(1)
                
                
        except KeyboardInterrupt:
            print("Quitting the program.")
        except:
            print("Unexpected error: "+str(sys.exc_info()[0]))
            raise
            
    def processFile(self, filepath):
        status = None
        try:
            status = self.statuses[filepath]
        except:
            pass
        
        if status is None:
            self.statuses[filepath] = "processing"
            try:
                #TODO Inference Watson and Raise a message with results
                print(filepath)
                self.sendImageToWatson(filepath)
            except:
                self.statuses[filepath] = "error"
                
    def sendImageToWatson(self, filepath):
        img = tf.keras.utils.img_to_array(tf.keras.utils.load_img(filepath))
        print(img.shape)
        
        wml_credentials = {
                   "url": watsonConfig["url"],
                   "apikey":watsonConfig["apiKey"]
                  }
        client = APIClient(wml_credentials)
        client.set.default_space(watsonConfig["spaceUID"])

        scoring_payload = {"input_data": [{"values": [img.tolist()]}]}

        predictions = client.deployments.score(watsonConfig["deploymentUID"], scoring_payload)

        print(json.dumps(predictions, indent=2))


if __name__ == '__main__':
    service = FileDropService()