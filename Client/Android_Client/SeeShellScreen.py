from kivy.uix.screenmanager import Screen
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import sys
sys.path.append('../')
import seeshell_client_common as common


# with open("config.json", "r") as f:
#     config = json.load(f)

class SeeShellScreen(Screen):
    '''
    Super class for all screens, holds the client API and message calling service functions
    '''
    # api = common.SeeShellAPIClient(config["apiURL"])
    #revert once server has static ip
    api = None
    @classmethod
    def setAPI(cls, ip):
        '''
        called on login to set API URL
        '''
        url = "http://{}:5000".format(ip)
        cls.api = common.SeeShellAPIClient(url)

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.jobs = []
        self.scheduler.start()

    def remove_job(self, id):
        '''
        removes scheduled job from scheduler
        '''
        self.jobs.remove(id)
        self.scheduler.remove_job(id)

    def check_message(self):
        '''
        Calls server to check for message, removes jobs for successfully identified images
        '''
        messages = SeeShellScreen.api.getMessages()
        for key in messages.keys():
            filepath = os.path.join('Photos', key + '.json')
            self.saveShellInfo(json.loads(messages[key]), filepath)
            try:
                self.remove_job(key)
            except ValueError:
                pass
            
    def check_for_identification(self, id, interval):
        '''
        Adds a job to the scheduler, checking for identification for a particular image
        '''
        self.scheduler.add_job(self.check_message, 'interval', seconds=interval, id=id)
        self.jobs.append(id)

    def get_current_jobs(self):
        return self.jobs

    def get_unmatched_images(self):
        '''
        Called on login, checks gallery for images that don't yet have identification and adds a job to the scheduler to check for id every 5 seconds
        '''
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
        '''
        saves retrieved shell info to a json with specified filename
        '''
        with open(filename, "w") as f:
            json.dump(message, f)