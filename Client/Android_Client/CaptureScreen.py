from SeeShellScreen import SeeShellScreen
from kivy.properties import ListProperty
from kivymd.uix.button import MDRoundFlatButton
from CropScreen import CropScreen
from kivy.app import App
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.uix.boxlayout import BoxLayout
from plyer import filechooser
import jnius
import os
import shutil
import uuid

class FileChoose(MDRoundFlatButton):
    selection = ListProperty([])
    screen = None
    def choose(self):
        filechooser.open_file(on_selection=self.handle_selection)
    def handle_selection(self, selection):
        self.selection = selection
    def on_selection(self, *args, **kwargs):
        CropScreen.targetImagePath = str(self.selection)
        FileChoose.screen.manager.current = "crop_screen"


class captureScreen(SeeShellScreen):
    images = ListProperty([])
    def on_pre_enter(self, *args):
        self.ids.camera.connect_camera(filepath_callback=self.mv_photo)
        FileChoose.screen = self

    def on_pre_leave(self):
        self.ids.camera.disconnect_camera()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.api = SeeShellScreen.api
        self.screen = self
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
        camera.capture_photo()
        print("Photo saved")