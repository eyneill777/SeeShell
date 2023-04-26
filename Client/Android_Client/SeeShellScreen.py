from kivy.uix.screenmanager import Screen
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import seeshell_client_common as common


# with open("config.json", "r") as f:
#     config = json.load(f)

class SeeShellScreen(Screen):
    # api = common.SeeShellAPIClient(config["apiURL"])
    #revert once server has static ip
    api = None
    @classmethod
    def setAPI(cls, ip):
        url = "http://{}:5000".format(ip)
        cls.api = common.SeeShellAPIClient(url)

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.jobs = []
        self.scheduler.start()

    def remove_job(self, id):
        self.jobs.remove(id)
        self.scheduler.remove_job(id)

    def check_message(self):
        messages = SeeShellScreen.api.getMessages()
        for key in messages.keys():
            filepath = os.path.join('Photos', key + '.json')
            self.saveShellInfo(json.loads(messages[key]), filepath)
            try:
                self.remove_job(key)
            except ValueError:
                pass
            
    def check_for_identification(self, id, interval):
        self.scheduler.add_job(self.check_message, 'interval', seconds=interval, id=id)
        self.jobs.append(id)

    def get_current_jobs(self):
        return self.jobs

    def get_unmatched_images(self):
        print('checking gallery for unmatched images')
        directory_path = 'Photos'
        files = {}
        for filename in os.listdir(directory_path):
            Id, filetype = filename.split('.')
            print(Id,filetype)
            if Id in files:
                files[Id].append(filetype)
            else:
                files[Id] = []
                files[Id].append(filetype)
        for Id in files:
            if len(files[Id]) == 1 and files[Id][0] != "json":
                self.check_for_identification(Id, 5)
        
    def saveShellInfo(self, message, filename):
        with open(filename, "w") as f:
            json.dump(message, f)