from SeeShellScreen import SeeShellScreen
from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.properties import ListProperty
from kivy.app import App
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
import os
import time
import uuid


class captureScreen(SeeShellScreen):
    images = ListProperty([])
    def __init__(self,api,**kwargs):
        #Builder.load_file('layout.kv')
        #self.screen_manager = manager
        super(captureScreen, self).__init__(**kwargs)
        self.camera = Camera(resolution = (640,480), play = True)
        print(self.camera)
        self.add_widget(self.camera)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.api = api


    def take_photo(self, *args):
        # camera = self.ids.camera
        img_id = str(uuid.uuid4())
        self.camera.export_to_png(f'Photos/{img_id}.png')
        with open(f'Photos/{img_id}.png', 'rb') as f:
            self.api.uploadImage(img_id,f,'user')
            f.close()
        popup = Popup(title='Success!', content=Label(text='Image uploaded, waiting \nfor identification.  You will be \nredirected to results when \nthey come in.'),
                      size_hint=(None, None), size=(200, 200))
        popup.open()
        super().check_for_identification(img_id, 5, self.api)
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
