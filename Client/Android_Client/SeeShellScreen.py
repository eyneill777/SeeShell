from kivy.uix.screenmanager import Screen
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import sys
import time
sys.path.append(os.path.abspath("../"))
import seeshell_client_common as common


with open("config.json", "r") as f:
    config = json.load(f)

class SeeShellScreen(Screen):
    api = common.SeeShellAPIClient(config["apiURL"])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.jobs = []

    def remove_job(self, id):
        self.jobs.remove(id)
        self.scheduler.remove_job(id)

    def check_message(self, id,dontknowwhythisisneeded):
        print('checking for matches')
        if SeeShellScreen.api.checkMessages(id):
            print('found match')
            filepath = 'Photos/{}.json'.format(id)
            SeeShellScreen.api.saveShellInfo(SeeShellScreen.api.getMessages(id), filepath)
            self.remove_job(id)
        else:
            print('no match yet')
    def check_for_identification(self, id, interval):
        self.scheduler.add_job(self.check_message, 'interval', seconds=interval, id = id, args=(id,''))
        self.jobs.append(id)

    def get_current_jobs(self):
        return self.jobs

    def get_unmatched_images(self):
        print('checking gallery for unmatched images')
        directory_path = 'Photos'
        files = {}
        for filename in os.listdir(directory_path):
            Id, filetype = filename.split('.')
            if Id in files:
                files[Id].append(filetype)
            else:
                files[Id] = []
                files[Id].append(filetype)
        for Id in files:
            if len(files[Id]) == 1:
                print('adding ' + Id + '.png to the joblist')
                self.jobs.append(Id)
                self.scheduler.add_job(self.check_message, 'interval', seconds=5, id=Id, args=(Id,''))
        self.scheduler.start()