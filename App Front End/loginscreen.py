from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import connection as c
from kivy.lang import Builder

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
        conn = c.dbconnection()
        cursor = conn.cursor(prepared=True)
        print(cursor)
        stmt = "Select * from User where Username = %s and password = %s"
        values = (self.email.text, self.password.text)
        print(values)
        cursor.execute(stmt, values)
        rows = cursor.fetchall()

        if len(rows) == 1:
            popup_content = Label(text='Login Successful')
            popup = Popup(title = 'Success!', content=popup_content,
                    size_hint = (None,None), size = (200,200))
            popup.open()
        else:
            popup = Popup(title='Error', content=Label(text='Invalid username or password'),
                          size_hint=(None, None), size=(200, 200))
            popup.open()

        if conn is not None and conn.is_connected():
            conn.close()

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

        #username
        self.add_widget(Label(text = 'Username'))
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
        else:
            #connect to database
            conn = c.dbconnection()
            cursor = conn.cursor(prepared = True)
            #insert user info into table
            stmt = "INSERT INTO User (Username,Email_Address, Password) VALUES (%s,%s,%s)"
            values = (username,email,password)
            cursor.execute(stmt, values)
            conn.commit()
            #verify that information was inserted
            ver_stmt = "SELECT * from user Where Email_Address = 'email'"
            cursor.execute(ver_stmt)
            rows = cursor.fetchall()

            if len(rows) == 1:
                popup_content_one = Label(text='Account Created')
                popup_one= Popup(title='Account Created', content=popup_content_one,
                              size_hint=(None, None), size=(200, 200))
                popup_one.open()
            else:
                popup_content_two = Label(text='Account Creation Failed')
                popup_two = Popup(title='Failed', content=popup_content_two,
                                  size_hint=(None, None), size=(200, 200))
                popup_two.open()

            conn.close()

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
        #add screens to screen manager
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(create_account_screen)

        return(screen_manager)



if __name__ == '__main__':
    MyApp().run()