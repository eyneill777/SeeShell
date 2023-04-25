from SeeShellScreen import SeeShellScreen
from kivy.uix.button import Button
from kivy.uix.image import Image
class CropScreen(SeeShellScreen):
    targetImagePath = None

    def on_pre_enter(self):
        self.crop_photo()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def crop_photo(self):
        self.add_widget(Image(source=CropScreen.targetImagePath,pos_hint={"center_y": .75}))
        self.add_widget(Button(text="Crop", size_hint=(1,.1), pos_hint={"center_y": .25}, on_release=self.to_capture_screen))

    def to_capture_screen(self, button):
        self.manager.current = "capture_screen"
