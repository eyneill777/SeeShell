import time
import sys
import os
import json
import random
import tensorflow as tf
from sqlalchemy import *
import traceback
from ibm_watson_machine_learning import APIClient
sys.path.append(os.path.abspath("../"))
import seeshell_server_common as common

with open("config.json", "r") as f:
    config = json.load(f)
    watsonConfig = config["watson"]

class FileDropService:
    
    def __init__(self):
        """
        Initialize the filedrop service.  Creates a database connection, prepares the class list that is used to categorize ML model responses, and begins the service's application loop.
        """
        self.engine = create_engine('mysql+pymysql://'+config['messageDB']['username']+':'+config['messageDB']['password']+'@'+config['messageDB']['host'])
        self.tables = common.Tables()
        self.generateClassList()
        self.watchFolder() #runs until stopped
    
    
    def watchFolder(self): 
        """
        Loops infinitely and checks the drop folder once per second.  If a file is found in the folder it is processed.
        """
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
    
    def generateClassList(self):
        """
        Prepares the class list that is used to categorize ML model responses.  Only runs once when the service is started.
        """
        print("loading class labels ...")
        self.classes = []
        train = tf.keras.utils.image_dataset_from_directory(
            config["datasetFolder"],
            labels='inferred', 
            label_mode='categorical', 
            color_mode='rgb', 
            subset="training",
            batch_size=128, 
            shuffle=True, 
            seed=123,
            validation_split=.1
            )
        self.classes = train.class_names
        print("Done")
    
    def processFile(self, filepath):
        """
        Sends files to watson for inference and handles responses based on result 
        """
        status = None
        try:
            status = self.statuses[filepath]
        except:
            pass
        
        if status is None:
            self.statuses[filepath] = "processing"
            try:
                result = self.sendImageToWatson(filepath)
                print(filepath)
                self.statuses[filepath] = "success"
                self.reportResults(os.path.basename(filepath).split("_")[1].split(".")[0], os.path.basename(filepath).split("_")[0], result)
            except Exception as e:
                self.statuses[filepath] = "error"
                self.reportError(filepath, "There was an error while classifying the file and reporting results.", e) #TODO add error types for various watson errors.
            self.cleanUp(filepath)
                
    def cleanUp(self, filepath):
        """
        Removes processed files from the input folder
        """
        if os.path.exists(filepath):
            os.remove(filepath)
        self.statuses.pop(filepath)
            
        
        
    def reportResults(self, id, username, classname):
        """
        Creates a message in the database with the results of a successful classification 
        """
        try:
            stmt = select(self.tables.Shell).where(self.tables.Shell.c.Scientific_Name == classname)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                dat = [r._asdict() for r in result][0]
                stmt = select(self.tables.Family).where(self.tables.Family.c.Family == dat["Family"])
                familyResult = conn.execute(stmt)
                for family in familyResult:
                    dat["Family_Link"] = family[1]
                js = json.dumps(dat)
                statement = insert(self.tables.Message).values(Id = id, Username = username, Data = js)
                conn.execute(statement)
                conn.commit()
                conn.close()
        except Exception as e:
            raise e
            
        
    def reportError(self, id, message, error): #TODO make this report a db message indicating an error
        """
        TODO function which reports a erroneous classification response back to the client 
        """
        print(message)
        traceback.print_exc()
                
    def sendImageToWatson(self, filepath): #TODO write code to process watson results into a class name when access is restored.
        """
        Handles Watson configuration and sends responses to the Watson API.  Categorization of responses is unfinished due to the denial of Watson service
        """
        if config["simulateResults"]:
            time.sleep(20)
            return random.choice(self.classes)
        else:
            img = tf.keras.utils.img_to_array(tf.keras.utils.load_img(filepath))
            print(img.shape)

            wml_credentials = {
                       "url": watsonConfig["url"],
                       "apikey":watsonConfig["apiKey"]
                      }
            client = APIClient(wml_credentials)
            client.set.default_space(watsonConfig["spaceUID"])

            scoring_payload = {"input_data": [{"values": [img.tolist()]}]}

            predictions = None
            try:
                predictions = client.deployments.score(watsonConfig["deploymentUID"], scoring_payload)
                print(predictions)
                #print(json.dumps(predictions, indent=2))

                
            except Exception as e:
                raise e


if __name__ == '__main__':
    service = FileDropService()