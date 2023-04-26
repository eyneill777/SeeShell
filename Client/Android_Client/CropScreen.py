from SeeShellScreen import SeeShellScreen
from kivy.uix.button import Button
from kivy.uix.image import Image
import cv2
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
        image = cv2.imread(CropScreen.targetImagePath)
        print(image.shape)
        height = image.shape[0]
        width = image.shape[1]
        if height/width > .75:
            num_pixels_to_remove = int((height-(width*.75))/2)
            image = image[num_pixels_to_remove:height-num_pixels_to_remove][::]
        else:
            'went in here'
            num_pixels_to_remove = int((width - (height * (4/3))) / 2)
            image = image[::][num_pixels_to_remove:width-num_pixels_to_remove]
        resized = cv2.resize(image, (400,300), interpolation=cv2.INTER_AREA)
        cv2.imwrite(CropScreen.targetImagePath, resized)
        with open(CropScreen.targetImagePath, 'rb') as f:
            SeeShellScreen.api.uploadImage(CropScreen.targetImagePath.split('/')[-1].split('.')[0], f)
            f.close()
        self.manager.current = "capture_screen"