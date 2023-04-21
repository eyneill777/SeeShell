from SeeShellScreen import SeeShellScreen
from kivy.lang import Builder


class blurbScreen(SeeShellScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api

    def get_species_info(self):
       pass