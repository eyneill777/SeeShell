from SeeShellScreen import SeeShellScreen
from kivy.properties import ListProperty
from kivymd.uix.button import MDRoundFlatButton
from CropScreen import CropScreen
from kivy.app import App
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.uix.boxlayout import BoxLayout
from plyer import filechooser
import jnius
import cv2
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
        file_path = str(self.selection).strip("['").strip("']")
        img_id = str(uuid.uuid4())
        FileChoose.screen.call_message_service(img_id)
        shutil.copy(file_path, 'Photos')
        filename = file_path.split('/')[-1]
        filetype = filename.split('.')[1]
        newname = "{}.{}".format(img_id,filetype)
        newpath = os.path.join('Photos', newname)
        oldpath = os.path.join('Photos', filename)
        os.rename(oldpath, newpath)
        CropScreen.targetImagePath = newpath
        FileChoose.screen.manager.current = "crop_screen"


class captureScreen(SeeShellScreen):
    images = ListProperty([])
    def on_pre_enter(self, *args):
        self.api = SeeShellScreen.api  ##remove when/if server on static IP
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
        filename = file_path.split('/')[-1]
        img_id = str(uuid.uuid4())
        image = cv2.imread(file_path)
        resized = cv2.resize(image, (400, 300), interpolation=cv2.INTER_AREA)
        cv2.imwrite(file_path, resized)
        with open(file_path, 'rb') as f:
            self.api.uploadImage(img_id, f)
            f.close()
        self.call_message_service(img_id)
        shutil.move(file_path, 'Photos')
        filetype = filename.split('.')[1]
        newname = "{}.{}".format(img_id, filetype)
        newpath = os.path.join('Photos', newname)
        oldpath = os.path.join('Photos', filename)
        os.rename(oldpath, newpath)

    def call_message_service(self, img_id):
        super().check_for_identification(img_id, 5)
    def take_photo(self, *args):
        camera = self.ids.camera
        camera.capture_photo()
        print("Photo saved")