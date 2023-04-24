from SeeShellScreen import SeeShellScreen
from kivy.properties import ListProperty
from kivy.app import App
from apscheduler.schedulers.background import BackgroundScheduler
from kivy.uix.boxlayout import BoxLayout
import os
import shutil
import uuid


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
        camera.capture_photo()
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