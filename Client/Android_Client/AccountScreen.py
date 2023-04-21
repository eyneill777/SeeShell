from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
import re
from kivy.uix.screenmanager import ScreenManager, Screen

class accountScreen(Screen):
    def __init__(self, api,**kwargs):
        Builder.load_file('create_account.kv')
        super(accountScreen, self).__init__(**kwargs)
        #self.manager = manager
        self.api = api

    def create_account(self):
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
