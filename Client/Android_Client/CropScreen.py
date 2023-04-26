from SeeShellScreen import SeeShellScreen
from kivy.uix.button import Button
from kivy.uix.image import Image
import PIL
import os
class CropScreen(SeeShellScreen):
    targetImagePath = None

    def on_pre_enter(self):
        self.load_photo()

    def on_leave(self, *args):
        self.ids.layout.clear_widgets()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_photo(self):
        self.ids.layout.add_widget(Image(source=CropScreen.targetImagePath, pos_hint={"center_y": .75}, nocache=True))
        self.ids.layout.add_widget(
            Button(text="Crop", size_hint=(1, .1), pos_hint={"center_y": .1}, on_release=self.crop_photo))
    def crop_photo(self,button):
        image = PIL.Image.open(CropScreen.targetImagePath)
        width, height = image.size
        if height/width > .75:

            num_pixels_to_remove = int((height-(width*.75))/2)
            image.crop((0, num_pixels_to_remove, width, height - num_pixels_to_remove)).save(
                CropScreen.targetImagePath)
        else:
            num_pixels_to_remove = int((width - (height * (4/3))) / 2)
            image.crop((num_pixels_to_remove, 0, width - num_pixels_to_remove, height)).save(
                CropScreen.targetImagePath)

        with open(CropScreen.targetImagePath, 'rb') as f:
            SeeShellScreen.api.uploadImage(CropScreen.targetImagePath.split('/')[-1].split('.')[0], f)
            f.close()
        self.manager.current = "capture_screen"