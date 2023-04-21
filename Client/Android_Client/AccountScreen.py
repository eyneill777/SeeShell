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

class accountScreen(FloatLayout):
    def __init__(self, manager,api,**kwargs):
        Builder.load_file('create_account.kv')
        super(accountScreen, self).__init__(**kwargs)
        self.manager = manager
        self.api = api

    def create_account(self, instance):
        email_input = self.ids.email_input
        username_input = self.ids.username_input
        password_input = self.ids.password_input
        ver_password_input = self.ids.ver_password_input

        email = email_input.text
        username = username_input.text
        password = password_input.text
        ver_password = ver_password_input.text

        #verify password
        if password != ver_password:
            popup_content = Label(text='Passwords do not match')
            popup = Popup(title='Invalid!', content=popup_content,
                          size_hint=(None, None), size=(200, 200))
            popup.open()
        #verify email
        elif not re.fullmatch(r'.+@.+\..+', email):
            popup_content = Label(text='Invalid email')
            popup = Popup(title='Invalid!', content=popup_content,
                          size_hint=(None, None), size=(200, 200))
            popup.open()
        else:
            responseText = self.api.createAccount(username, email, password)
            if responseText == 'Success':
                self.manager.current = 'capture_screen'
            else:
                popup = Popup(title='Error', content=Label(text=responseText),
                              size_hint=(None, None), size=(200, 200))
                popup.open()
