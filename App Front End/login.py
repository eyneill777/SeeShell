from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.toast import toast
from sqlalchemy import *
import json

class Login(Screen):
    pass
    def connect(self):
        #get email and password from Screen
        app = App.get_running_app()
        input_email = app.manager.get_screen('login').ids['input_email'].text
        input_password = app.manager.get_screen('login').ids['input_password'].text

        with open("config.json", "r") as f:
            config = json.load(f)

        engine = create_engine('mysql://' + config['Username'] + ':' + config['Password'] + '@' + config['host'])

        with engine.connect() as conn:
            result = conn.execute(text("select password from user where Username =" + input_email))
            print(result)

        #verif login/email
        #if invalid
        if count == 0:
            toast('Invalid Login/Password')
        #else, if valid
        else:
            toast('Login and Password are correct!')
        pass