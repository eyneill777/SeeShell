from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.app import App
import time
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
#from kivy.lang import Builder
import requests
import re
import os
import json
import sys
from kivymd.app import MDApp
from kivy.uix.image import AsyncImage
sys.path.append(os.path.abspath("../"))
import seeshell_client_common as common

with open("config.json", "r") as f:
    config = json.load(f)


api = common.SeeShellAPIClient(config["apiURL"])


class LoginScreen(FloatLayout):

    def __init__(self,manager,**kwargs):
        Builder.load_file('login.kv')
        super(LoginScreen, self).__init__(**kwargs)
        self.manager = manager

    def authenticate(self, instance):
        print('authentication called')
        email_input = self.ids.email_input
        password_input = self.ids.password_input

        email = email_input.text
        password = password_input.text

        responseText = api.checkPass(email, password)
        if responseText == 'Success':
            popup_content = Label(text='Login Successful')
            popup = Popup(title = 'Success!', content=popup_content,
                    size_hint = (None,None), size = (200,200))
            popup.open()
            self.manager.current = 'capture_screen'

        else:
            popup = Popup(title='Error', content=Label(text=responseText),
                              size_hint=(None, None), size=(200, 200))
            popup.open()

    def go_to_create_account(self, instance):
        self.manager.current = 'create_account_screen'



class accountScreen(FloatLayout):
    def __init__(self, manager,**kwargs):
        Builder.load_file('create_account.kv')
        super(accountScreen, self).__init__(**kwargs)
        self.manager = manager

    def create_account(self, instance):
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
            responseText = api.createAccount(username, email, password)
            if responseText == 'Success':
                self.manager.current = 'capture_screen'
            else:
                popup = Popup(title='Error', content=Label(text=responseText),
                              size_hint=(None, None), size=(200, 200))
                popup.open()


class captureScreen(Screen):
    images = ListProperty([])
    def __init__(self,manager,**kwargs):
        Builder.load_file('capture.kv')
        self.manager = manager
        super(captureScreen, self).__init__(**kwargs)
        self.camera = Camera(resolution = (640,480), play = True)
        self.add_widget(self.camera)

    def take_photo(self, *args):
        #camera = self.ids.camera
        time_str = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png(f'IMG_{time_str}.png')
        print("Photo saved")

    def add_image(self, *args):
        # open a file selection dialog and get the selected file
        from kivy.uix.filechooser import FileChooserIconView
        chooser = FileChooserIconView()
        chooser.path = os.path.expanduser('~')
        chooser.filters = ['*.png', '*.jpg', '*.jpeg']
        chooser.bind(selection=self.load_image)
        popup = BoxLayout()
        popup.add_widget(chooser)
        App.get_running_app().root_window.add_widget(popup)

    def load_image(self, chooser, selection):
        if selection:
            # create a new selectable image widget and add it to the album
            img = SelectableImage(source=selection[0], allow_stretch=True)
            # resize images
            # self.img.AsyncImage(size_hint=(None, None), size=(200, 200))
            self.images.append(img)
            self.add_widget(img)
        chooser.parent.parent.remove_widget(chooser.parent)
    def switch_to_album(self, instance):
        self.manager.current = 'gallery_screen'

    def go_to_blurb_screen(self,instance):
        self.manager.current = 'blurb_screen'

class blurbScreen(Screen):
    def __init__(self,manager,**kwargs):
        Builder.load_file('blurb.kv')
        self.manager = manager
        super(blurbScreen, self).__init__(**kwargs)

class SelectableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SelectableImage, self).__init__(**kwargs)
        self.allow_stretch = True

    def on_press(self):
        '''
        method that is added to the image widgets to change the color of the
        widget when clicked
        '''
        # toggles the 'selected' attribute
        self.selected = not self.selected
        if self.selected:
            animation = Animation(color=(1, 0, 0, 1), duration=0.25)
            animation.start(self)
        else:
            animation = Animation(color=(1, 1, 1, 1), duration=0.25)
            animation.start(self)


class PhotoAlbum(GridLayout):
    images = ListProperty([])
    Builder.load_file('gallery.kv')
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.screen_manager = manager
        super(PhotoAlbum, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 10

    def go_to_camera_screen(self, instance):
       self.screen_manager.current = 'capture_screen'

    def delete_image(self, instance):
        selected_widgets = [widget for widget in self.images if widget.selected]
        for widget in selected_widgets:
            self.remove_widget(widget)
            self.images.remove(widget)


class MyApp(MDApp):
    def build(self):
        Window.size = (360,640)
        screen_manager = ScreenManager()
        #create login screen
        login_screen = Screen(name = 'login')
        login_layout = LoginScreen(manager = screen_manager)
        login_screen.add_widget(login_layout)
        # #create account screen
        create_account_screen = Screen(name = 'create_account_screen')
        create_account_layout = accountScreen(manager = screen_manager)
        create_account_screen.add_widget(create_account_layout)
        # #create capture mode screen
        capture_screen = Screen(name = 'capture_screen')
        capture_layout = captureScreen(manager = screen_manager)
        capture_screen.add_widget(capture_layout)
        # #create capture mode screen
        blurb_screen = Screen(name='blurb_screen')
        blurb_layout = blurbScreen(manager=screen_manager)
        blurb_screen.add_widget(blurb_layout)
        # #create gallery screen (gallery_screen)
        gallery_screen = Screen(name = 'gallery_screen')
        gallery_screen_layout = PhotoAlbum(manager = screen_manager)
        gallery_screen.add_widget(gallery_screen_layout)
        #add screens to screen manager
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(create_account_screen)
        screen_manager.add_widget(capture_screen)
        screen_manager.add_widget(blurb_screen)
        screen_manager.add_widget(gallery_screen)



        return(screen_manager)


if __name__ == '__main__':
    MyApp().run()