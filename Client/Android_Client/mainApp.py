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
import seeshell_client_common as common
import AccountScreen
import LoginScreen
import CaptureScreen
import GalleryScreen
import BlurbScreen

with open("config.json", "r") as f:
    config = json.load(f)


api = common.SeeShellAPIClient(config["apiURL"])


class MyApp(MDApp):

    def build(self):
        Window.size = (360,640)
        screen_manager = ScreenManager()
        #create login screen
        login_screen = Screen(name = 'login')
        login_layout = LoginScreen.LoginScreen(manager=screen_manager, api=api)
        login_screen.add_widget(login_layout)
        # #create account screen
        create_account_screen = Screen(name = 'create_account_screen')
        create_account_layout = AccountScreen.accountScreen(manager=screen_manager, api=api)
        create_account_screen.add_widget(create_account_layout)
        # #create capture mode screen
        capture_screen = Screen(name = 'capture_screen')
        capture_layout = CaptureScreen.captureScreen(manager=screen_manager, api=api)
        capture_screen.add_widget(capture_layout)
        # #create capture mode screen
        blurb_screen = Screen(name='blurb_screen')
        blurb_layout = BlurbScreen.blurbScreen(manager=screen_manager, api=api)
        blurb_screen.add_widget(blurb_layout)
        # #create gallery screen (gallery_screen)
        gallery_screen = Screen(name = 'gallery_screen')
        gallery_screen_layout = GalleryScreen.PhotoAlbum(manager=screen_manager, api=api)
        gallery_screen.add_widget(gallery_screen_layout)
        #add screens to screen manager
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(create_account_screen)
        screen_manager.add_widget(capture_screen)
        screen_manager.add_widget(blurb_screen)
        screen_manager.add_widget(gallery_screen)

        return screen_manager


if __name__ == '__main__':
    MyApp().run()