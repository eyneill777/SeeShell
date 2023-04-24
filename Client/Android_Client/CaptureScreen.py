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
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
import camera4kivy
import os
import shutil
import time
import uuid
from PIL import Image


class captureScreen(SeeShellScreen):
    images = ListProperty([])
    def on_pre_enter(self, *args):
        self.ids.camera.connect_camera(filepath_callback=self.mv_photo)
    def on_pre_leave(self):
        self.ids.camera.disconnect_camera()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.api = SeeShellScreen.api
    def mv_photo(self, file_path):
        print('called')
        filename = file_path.split('/')[-1]
        img_id = str(uuid.uuid4())
        with open(file_path, 'rb') as f:
            self.api.uploadImage(img_id, f)
            f.close()
        shutil.move(file_path, 'Photos')
        newname = "{}.jpg".format(img_id)
        newpath = os.path.join('Photos', newname)
        oldpath = os.path.join('Photos', filename)
        os.rename(oldpath, newpath)

    def take_photo(self, *args):
        camera = self.ids.camera
        img_id = str(uuid.uuid4())
        camera.capture_photo()
        # camera.texture.save(f'Photos/{img_id}.png')
        # with open(f'Photos/{img_id}.png', 'rb') as f:
        #     self.api.uploadImage(img_id,f)
        #     f.close()
        # popup = Popup(title='Success!', content=Label(text='Image uploaded, waiting\nfor identification.  You\ncan check results\nin the gallery.'),
        #               size_hint=(None, None), size=(200, 200))
        # popup.open()
        # super().check_for_identification(img_id, 5)
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