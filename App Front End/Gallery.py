import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from plyer import filechooser
from kivy.uix.floatlayout import FloatLayout


class PhotoAlbum(App):
    def build(self):
        # create the main layout
        main_layout = BoxLayout(orientation='vertical')

        # create a list to store the images
        self.images = []
