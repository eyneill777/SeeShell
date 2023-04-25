from kivy.uix.label import Label
from kivy.uix.popup import Popup
from apscheduler.schedulers.background import BackgroundScheduler
from SeeShellScreen import SeeShellScreen

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
            self.api.username = email
            self.check_message()
            super().get_unmatched_images()
            self.manager.current = 'capture_screen'

        else:
            popup = Popup(title='Error', content=Label(text=responseText),
                              size_hint=(None, None), size=(200, 200))
            popup.open()


