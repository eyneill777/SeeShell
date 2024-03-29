from kivy.uix.label import Label
from kivy.uix.popup import Popup
from apscheduler.schedulers.background import BackgroundScheduler
from SeeShellScreen import SeeShellScreen
import time

class LoginScreen(SeeShellScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.api = SeeShellScreen.api


    def authenticate(self):
        '''
        Captures user input and provides it to API client to validate
        '''
        SeeShellScreen.setAPI(self.ids.ip_input.text)  ##remove when/if server on static IP
        self.api = SeeShellScreen.api  ##remove when/if server on static IP
        print('authentication called')
        email_input = self.ids.email_input
        password_input = self.ids.password_input

        email = email_input.text
        password = password_input.text

        responseText = self.api.checkPass(email, password)

        if responseText == 'Success':
            self.api.username = email
            self.manager.current = 'capture_screen'

        else:
            popup = Popup(title='Error', content=Label(text=responseText),
                              size_hint=(None, None), size=(500, 150))
            popup.open()


