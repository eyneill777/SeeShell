from SeeShellScreen import SeeShellScreen
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
import kivy.core.text.markup
import os
import webbrowser
import json
import base64


class blurbScreen(SeeShellScreen):
    target = None
    def on_pre_enter(self, *args):
        '''
        Called when entering the screen, populates the screen with captured shell image and relevant information about it if it has been identified
        '''
        self.api = SeeShellScreen.api  ##remove when/if server on static IP
        if not self.has_info(blurbScreen.target.split('.')[0]):
            self.ids.blurb_label.text = "We haven't gotten this shell \nidentified yet. Please check back later."
            img_file_path = os.path.join('Photos', blurbScreen.target)
        else:
            id = blurbScreen.target.split('.')[0]
            json_file_path = os.path.join('Photos', id+'.json')
            img_file_path = os.path.join('Photos', blurbScreen.target)
            with open(json_file_path, 'r') as f:
                shell_dict = json.load(f)
            map_file_path = os.path.join("Maps", shell_dict["Scientific_Name"]+'.png')
            shell_dict = self.api.clean_data(shell_dict)
            og_pos = self.get_parent_window().height/8
            for key in shell_dict:
                if key == "Family" and "Family_Link" in shell_dict:
                    link = shell_dict["Family_Link"]
                    text = "{}: [ref={}][u][color=#0000EE]{}[/color][/u][/ref]".format(key,link,shell_dict[key])
                    self.ids.layout.add_widget(
                        MDLabel(text=text, font_name="assets/poppins/Poppins-SemiBold.ttf",
                                pos=(0, og_pos), halign="center", markup=True, on_ref_press=self.go_to_link))
                else:
                    if key == "Family_Link":
                        continue
                    text = "{}: {}".format(key,shell_dict[key])
                    self.ids.layout.add_widget(MDLabel(text=text, font_name="assets/poppins/Poppins-SemiBold.ttf",
                                            pos=(0,og_pos), halign="center"))
                og_pos -= self.get_parent_window().height/20
            self.ids.blurb_label.text = ""
            if os.path.isfile(map_file_path):
                self.ids.layout.add_widget(Image(source=map_file_path, pos=(0, og_pos-self.get_parent_window().height/20)))
        self.ids.layout.add_widget(Image(source=img_file_path, size_hint=(.75,.5625), pos_hint={"center_x": .5, "top":1.1}))

    def on_leave(self, *args):
        self.ids.layout.clear_widgets()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api

    def has_info(self, shell):
        '''
        Checks for shell identification status
        '''
        if shell is None:
            return False
        directory_path = 'Photos'
        file_path = os.path.join(directory_path, shell + '.json')
        if os.path.isfile(file_path):
           return True
        return False

    def go_to_link(self,label,link):
        '''
        Opens up clickable link
        '''
        webbrowser.open(link)