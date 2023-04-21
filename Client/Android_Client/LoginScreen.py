from kivy.uix.label import Label
from kivy.uix.popup import Popup
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from SeeShellScreen import SeeShellScreen
import os
import sys
sys.path.append(os.path.abspath("../"))


class LoginScreen(SeeShellScreen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.api = SeeShellScreen.api


    def authenticate(self):
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
                super().get_unmatched_images()
                self.manager.current = 'capture_screen'

        else:
            popup = Popup(title='Error', content=Label(text=responseText),
                              size_hint=(None, None), size=(200, 200))
            popup.open()

    #def go_to_create_account(self):
        #pass
        #self.manager.current = 'create_account_screen'