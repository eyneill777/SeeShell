from SeeShellScreen import SeeShellScreen
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
import os
import json


class blurbScreen(SeeShellScreen):
    target = None
    def on_pre_enter(self, *args):
        self.api = SeeShellScreen.api  ##remove when/if server on static IP
        if not self.has_info(blurbScreen.target):
            self.ids.blurb_label.text = "We haven't gotten this shell identified yet.  Please check back later"
        else:
            for filename in os.listdir('Photos'):
                if blurbScreen.target in filename and filename.split('.')[1] == 'json':
                    json_file_path = os.path.join('Photos', filename)
                if blurbScreen.target in filename and 'map' in filename:
                    map_file_path = os.path.join('Photos', filename)
                elif blurbScreen.target in filename and filename.split('.')[1] != 'json':
                    img_file_path = os.path.join('Photos', filename)
            with open(json_file_path, 'r') as f:
                shell_dict = json.load(f)
            shell_dict = self.api.clean_data(shell_dict)
            og_pos = self.get_parent_window().height/8
            for key in shell_dict:
                text = "{}: {}".format(key,shell_dict[key])
                self.add_widget(MDLabel(text=text, font_style="H4", font_name="assets/poppins/Poppins-SemiBold.ttf",
                                        pos=(0,og_pos), halign="center"))
                og_pos -= self.get_parent_window().height/20
            self.ids.blurb_label.text = ""

        self.add_widget(Image(source=img_file_path, size_hint=(.75,.5625), pos_hint={"center_x": .5, "top":1.1}))
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api

    def has_info(self, shell):
        if shell is None:
            return False
        directory_path = 'Photos'
        file_path = os.path.join(directory_path, shell + '.json')
        if os.path.isfile(file_path):
           return True
        return False