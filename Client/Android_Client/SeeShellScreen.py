from kivy.uix.screenmanager import Screen
from apscheduler.schedulers.background import BackgroundScheduler

class SeeShellScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self._jobs = []

    def remove_job(self, id):
        self.scheduler.remove_job(id)
        self._jobs.remove(id)
        if len(self._jobs) == 0:
            self.scheduler.shutdown()

    def check_message(self, id, api):
        print('checking for messages')
        if api.checkMessages(id):
            print('found message')
            api.getMessages(id)
            self.remove_job(id)
        print('no messages')
    def check_for_identification(self, id, interval, api):
        self.scheduler.add_job(self.check_message, 'interval', seconds=interval, args=(id,api))
        self._jobs.append(id)

    def get_current_jobs(self):
        return self._jobs
