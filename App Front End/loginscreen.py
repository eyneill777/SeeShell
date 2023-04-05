from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera
from kivy.lang import Builder
import requests
import re

class LoginScreen(GridLayout):

    def __init__(self,manager,**kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.manager = manager
        #username
        self.add_widget(Label(text = 'Email'))
        self.email = TextInput(multiline = False)
        self.add_widget(self.email)
        #password
        self.add_widget(Label(text =  'Password'))
        self.password = TextInput(password = True, multiline = False)
        self.add_widget(self.password)
        #submit button
        self.submit = Button(text = 'Login')
        self.submit.bind(on_press = self.authenticate)
        self.add_widget(Label())
        self.add_widget(self.submit)
        #new account button
        self.createAccount = Button(text = "Create Account")
        self.createAccount.bind(on_press = self.go_to_create_account)
        self.add_widget(Label())
        self.add_widget(self.createAccount)

    def authenticate(self, instance):
        username, password = self.email.text, self.password.text
        headers = {"username": username, "password": password}
        try:
            response = requests.post("http://localhost:5000/checkPass/", headers=headers)
            if response.text == 'good':
                popup_content = Label(text='Login Successful')
                popup = Popup(title = 'Success!', content=popup_content,
                        size_hint = (None,None), size = (200,200))
                popup.open()
                self.manager.current = 'capture_screen'

            else:
                popup = Popup(title='Error', content=Label(text='Invalid username or password'),
                              size_hint=(None, None), size=(200, 200))
                popup.open()
        except requests.exceptions.ConnectionError:
            popup = Popup(title='Error', content=Label(text='Connection to server failed'),
                  size_hint=(None, None), size=(200, 200))
            popup.open()

    def go_to_create_account(self, instance):
        self.manager.current = 'create_account_screen'



class accountScreen(GridLayout):
    def __init__(self, manager,**kwargs):
        super(accountScreen, self).__init__(**kwargs)
        self.cols = 2
        #email
        self.add_widget(Label(text = 'Email'))
        self.email = TextInput(multiline = False)
        self.add_widget(self.email)

        # username
        self.add_widget(Label(text='Username'))
        self.username = TextInput(multiline = False)
        self.add_widget(self.username)

        # password
        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        # verify password
        self.add_widget(Label(text='Verify Password'))
        self.ver_password = TextInput(password=True, multiline=False)
        self.add_widget(self.ver_password)

        # submit button
        self.submit = Button(text='Create Account')
        self.submit.bind(on_press=self.create_account)
        self.add_widget(Label())
        self.add_widget(self.submit)

    def create_account(self, instance):
        email = self.email.text
        username = self.username.text
        ver_password = self.ver_password.text
        password = self.password.text

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
            try:
                headers = {"username": username, "email": email, "password": password}
                response = requests.post("http://localhost:5000/createAccount/", headers=headers)
                print(response.text)
                if response.text == 'Username taken':
                    popup = Popup(title='Error', content=Label(text='Username taken, please try another'),
                                  size_hint=(None, None), size=(200, 200))
                    popup.open()
                elif response.text == 'Success':
                    print("Data inserted successfully")
                    self.manager.current = 'capture_screen'
                else:
                    print("Data insertion failed")
            except requests.exceptions.ConnectionError:
                popup = Popup(title='Error', content=Label(text='Connection to server failed'),
                              size_hint=(None, None), size=(200, 200))
                popup.open()


class captureScreen(Screen):
    def __init__(self,**kwargs):
        super(captureScreen, self).__init__(**kwargs)
        self.camera = Camera(resolution = (640,480), play = True)
        self.add_widget(self.camera)
class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        #create login screen
        login_screen = Screen(name = 'login')
        login_layout = LoginScreen(manager = screen_manager)
        login_screen.add_widget(login_layout)
        #create account screen
        create_account_screen = Screen(name = 'create_account_screen')
        create_account_layout = accountScreen(manager = screen_manager)
        create_account_screen.add_widget(create_account_layout)
        #create capture mode screen
        capture_screen = Screen(name = 'capture_screen')
        capture_layout = captureScreen()
        capture_screen.add_widget(capture_layout)
        #add screens to screen manager
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(create_account_screen)
        screen_manager.add_widget(capture_screen)


        return(screen_manager)


if __name__ == '__main__':
    MyApp().run()