from kivy.app import App
from kivy.clock import mainthread
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.app import App
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
#from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.image import AsyncImage
import requests
import re
import os
import json
import sys
import time
sys.path.append(os.path.abspath("../"))


class SelectableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SelectableImage, self).__init__(**kwargs)
        self.allow_stretch = True

    def on_press(self):
        '''
        method that is added to the image widgets to change the color of the
        widget when clicked
        '''
        # toggles the 'selected' attribute
        self.selected = not self.selected
        if self.selected:
            animation = Animation(color=(1, 0, 0, 1), duration=0.25)
            animation.start(self)
        else:
            animation = Animation(color=(1, 1, 1, 1), duration=0.25)
            animation.start(self)


class PhotoAlbum(GridLayout):
    images = ListProperty([])
    Builder.load_file('gallery.kv')
    def __init__(self, manager,api, **kwargs):
        self.manager = manager
        self.screen_manager = manager
        super(PhotoAlbum, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 10
        self.api = api

    def go_to_camera_screen(self, instance):
       self.screen_manager.current = 'capture_screen'

    def delete_image(self, instance):
        selected_widgets = [widget for widget in self.images if widget.selected]
        for widget in selected_widgets:
            self.remove_widget(widget)
            self.images.remove(widget)
