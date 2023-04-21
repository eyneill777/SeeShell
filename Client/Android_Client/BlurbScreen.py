from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


class blurbScreen(Screen):
    def __init__(self,api,**kwargs):
        Builder.load_file('blurb.kv')
        #self.screen_manager = manager
        super(blurbScreen, self).__init__(**kwargs)
        self.api = api

    def get_species_info(self):
       pass
