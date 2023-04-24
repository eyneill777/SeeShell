from SeeShellScreen import SeeShellScreen
from kivy.uix.image import Image
import os
import json


class blurbScreen(SeeShellScreen):
    target = None
    def on_pre_enter(self, *args):
        self.ids.blurb_label.text = self.get_species_info(blurbScreen.target)
        for filename in os.listdir('Photos'):
            if blurbScreen.target in filename and filename.split('.')[1] != '.json':
                file_path = os.path.join('Photos', filename)
                break
        self.add_widget(Image(source=file_path, pos_hint = {"top": 1.35}))
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api

    def get_species_info(self, shell):
        if shell is None:
            return "This is where shell info will go"
        directory_path = 'Photos'
        file_path = os.path.join(directory_path, shell + '.json')
        if not os.path.isfile(file_path):
           return "We haven't gotten this shell identified yet.  Please check back later"
        with open(file_path, 'r') as f:
            shellData = json.load(f)
        return self.api.makeBlurb(shellData)
