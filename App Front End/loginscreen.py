from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import requests
import re
Window.size = (350, 580)


class LoginPage(MDApp):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("login.kv"))
        return screen_manager

    def on_start(self):
        Clock.schedule_once(self.login, 5)

    def login(self, *args):
        screen_manager.current = "login"

    def authenticate(self):
        username, password = self.email.text, self.password.text
        headers = {"username": username, "password": password}
        try:
            response = requests.post(
                "http://localhost:5000/checkPass/", headers=headers)
            if response.text == 'good':
                popup_content = Popup(title='Success!', content=Label(text='Login Successful'),
                                      size_hint=(None, None), size=(200, 200))
                popup_content.open()
                self.manager.current = 'capture_screen'

            else:
                popup_content = Popup(title='Error', content=Label(text='Invalid username or password'),
                                      size_hint=(None, None), size=(200, 200))
                popup_content.open()
        except requests.exceptions.ConnectionError:
            popup_content = Popup(title='Error', content=Label(text='Connection to server failed'),
                                  size_hint=(None, None), size=(200, 200))
            popup_content.open()

    def go_to_create_account(self):
        self.manager.current = 'create_account_screen'


class accountScreen(GridLayout):

    def __init__(self, manager, **kwargs):
        super(accountScreen, self).__init__(**kwargs)
        self.manager = manager

    def create_account(self):
        email = self.ids.email.text
        username = self.ids.username.text
        ver_password = self.ids.ver_password.text
        password = self.ids.password.text

        # verify password
        if password != ver_password:
            popup_content = Popup(title='Invalid!', content=Label(text='Passwords do not match'),
                                  size_hint=(None, None), size=(200, 200))
            popup_content.open()
        # verify email
        elif not re.fullmatch(r'.+@.+\..+', email):
            popup_content = Popup(title='Invalid!', content=Label(text='Invalid email'),
                                  size_hint=(None, None), size=(200, 200))
            popup_content.open()
        else:
            try:
                headers = {"username": username,
                           "email": email, "password": password}
                response = requests.post(
                    "http://localhost:5000/createAccount/", headers=headers)

                if response.text == 'Success':
                    print("Data inserted successfully")
                    self.manager.current = 'capture_screen'
                else:
                    print("Data insertion failed")
            except requests.exceptions.ConnectionError:
                popup_content = Popup(title='Error', content=Label(text='Connection to server failed'),
                                      size_hint=(None, None), size=(200, 200))
                popup_content.open()


class captureScreen(Screen):
    pass


class MyApp(App):
    def build(self):
        Builder.load_file('login.kv')
        screen_manager = ScreenManager()

        # create login screen
        login_screen = Screen(name='login')
        login_layout = LoginPage(manager=screen_manager)
        login_screen.add_widget(login_layout)

        # create account screen
        create_account_screen = Screen(name='create_account_screen')
        create_account_layout = accountScreen(manager=screen_manager)
        create_account_screen.add_widget(create_account_layout)

        # create capture mode screen
        capture_screen = Screen(name='capture_screen')
        # capture_layout = captureScreen()


if __name__ == "__main__":
    LoginPage().run()
