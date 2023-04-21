from kivy.uix.label import Label
from kivy.uix.popup import Popup
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
import os
import sys
sys.path.append(os.path.abspath("../"))


class LoginScreen(FloatLayout):

    def __init__(self,manager,api,**kwargs):
        Builder.load_file('login.kv')
        super(LoginScreen, self).__init__(**kwargs)
        self.manager = manager
        self.scheduler = BackgroundScheduler()
        self.api = api


    def authenticate(self, instance):
        print('authentication called')
        email_input = self.ids.email_input
        password_input = self.ids.password_input

        email = email_input.text
        password = password_input.text

        responseText = self.api.checkPass(email, password)
        if responseText == 'Success':
            popup_content = Label(text='Login Successful')
            popup = Popup(title = 'Success!', content=popup_content,
                    size_hint = (None,None), size = (200,200))
            popup.open()
            if self.api.checkMessages(email):
                self.manager.current = 'blurb_screen'
            else:
                self.manager.current = 'capture_screen'

        else:
            popup = Popup(title='Error', content=Label(text=responseText),
                              size_hint=(None, None), size=(200, 200))
            popup.open()

    def go_to_create_account(self, instance):
        self.manager.current = 'create_account_screen'
