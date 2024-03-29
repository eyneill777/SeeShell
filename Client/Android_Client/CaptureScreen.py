from SeeShellScreen import SeeShellScreen
from kivy.properties import ListProperty
from kivymd.uix.button import MDRoundFlatButton
from CropScreen import CropScreen
from kivy.app import App
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.uix.boxlayout import BoxLayout
from plyer import filechooser
import jnius
import PIL
import os
import shutil
import uuid



class LogOut(MDRoundFlatButton):
    def logout(self, instance):
        # clear user session and return to the login screen
        # session.clear()
        self.manager.current('LoginScreen')



class FileChoose(MDRoundFlatButton):
    selection = ListProperty([])
    screen = None
    def choose(self):
        filechooser.open_file(on_selection=self.handle_selection)
    def handle_selection(self, selection):
        self.screen.on_selection(selection)

    # currently broken on Android, need to fix in future
    # def on_selection(self, *args, **kwargs):
        # file_path = str(self.selection).strip("['").strip("']")
        # img_id = str(uuid.uuid4())
        # FileChoose.screen.call_message_service(img_id)
        # shutil.copy(file_path, 'Photos')
        # filename = file_path.split('/')[-1]
        # filetype = filename.split('.')[1]
        # newname = "{}.{}".format(img_id,filetype)
        # newpath = os.path.join('Photos', newname)
        # oldpath = os.path.join('Photos', filename)
        # os.rename(oldpath, newpath)
        # CropScreen.targetImagePath = newpath
        # FileChoose.screen.manager.current = "crop_screen"


class captureScreen(SeeShellScreen):
    images = ListProperty([])
    def on_pre_enter(self, *args):
        '''
        On enter checks for unidentified images and calls the message checking service, then connects camera
        '''
        if self.check_images:
            self.check_images = False
            super().get_unmatched_images()
        self.api = SeeShellScreen.api  ##remove when/if server on static IP
        self.ids.camera.connect_camera(filepath_callback=self.mv_photo)
        FileChoose.screen = self

    def on_pre_leave(self):
        '''
        Disconnects camera when leaving screen
        '''
        self.ids.camera.disconnect_camera()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.check_images = True
        self.api = SeeShellScreen.api

    def mv_photo(self, file_path):
        '''
        Moves captured photo into the Photos folder from the automatically generated date folder upon image capture
        '''
        im = PIL.Image.open(file_path)
        im = im.convert('RGBA')
        new_file_path = file_path.split('.')[0]+'.png'
        im.save(new_file_path, format='PNG')
        filename = new_file_path.split('/')[-1]
        img_id = str(uuid.uuid4())
        with open(file_path, 'rb') as f:
            self.api.uploadImage(img_id, f)
            f.close()
        self.call_message_service(img_id)
        shutil.move(new_file_path, 'Photos')
        os.remove(file_path)
        shutil.rmtree(file_path.split('/')[-2])
        newname = "{}.png".format(img_id)
        newpath = os.path.join('Photos', newname)
        oldpath = os.path.join('Photos', filename)
        os.rename(oldpath, newpath)


    def call_message_service(self, img_id):
        '''
        Calls SeeShellScreen's check for id for the specified image on a 5 second interval
        '''
        super().check_for_identification(img_id, 5)
    def take_photo(self, *args):
        '''
        Captures image
        '''
        camera = self.ids.camera
        camera.capture_photo(location="private")
        camera.capture_photo()

    # currently broken on Android, need to fix in future
    def on_selection(self, selection):
        '''
        Copies uploaded photo into Photos folder then sends you to crop screen
        '''
        print(selection)
        file_path = str(selection).strip("['").strip("']")
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
        self.manager.current = "crop_screen"