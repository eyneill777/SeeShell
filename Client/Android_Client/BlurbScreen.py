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


class blurbScreen(Screen):
    def __init__(self,manager,api,**kwargs):
        Builder.load_file('blurb.kv')
        self.manager = manager
        super(blurbScreen, self).__init__(**kwargs)
        self.api = api
