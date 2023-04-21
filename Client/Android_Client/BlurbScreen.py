from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


class blurbScreen(Screen):
    def __init__(self,manager,api,**kwargs):
        Builder.load_file('blurb.kv')
        self.manager = manager
        super(blurbScreen, self).__init__(**kwargs)
        self.api = api
