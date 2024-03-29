from SeeShellScreen import SeeShellScreen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import re

class accountScreen(SeeShellScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api

    def create_account(self):
        '''
        Collects user input then passes to API client for account creation and validation, pops up error causes when an error is detected
        '''
        SeeShellScreen.setAPI(self.ids.ip_input.text)  ##remove when/if server on static IP
        self.api = SeeShellScreen.api  ##remove when/if server on static IP
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
        elif '@' in username:
            popup_content = Label(text='Username may not\ncontain @ symbol')
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