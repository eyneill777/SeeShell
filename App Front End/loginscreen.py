from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import mysql.connector
from mysql.connector import Error
import connection as c

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        #username
        self.add_widget(Label(text = 'User Name'))
        self.username = TextInput(multiline = False)
        self.add_widget(self.username)
        #password
        self.add_widget(Label(text =  'password'))
        self.password = TextInput(password = True, multiline = False)
        self.add_widget(self.password)
        #submit buttom
        self.submit = Button(text = 'Login')
        self.submit.bind(on_press = self.authenticate)
        self.add_widget(Label())
        self.add_widget(self.submit)

    def authenticate(self, instance):
        conn = None
        conn = c.dbconnection()
        cursor = conn.cursor(prepared=True)
        print(cursor)
        stmt = "Select * from user where Username = %s and password = %s"
        values = (self.username.text, self.password.text)
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

class MyApp(App):
    def build(self):
        return(LoginScreen())



if __name__ == '__main__':
    MyApp().run()