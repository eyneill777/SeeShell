from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.lang import Builder
from SeeShellScreen import SeeShellScreen
import os


class SelectableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SelectableImage, self).__init__(**kwargs)
        self.allow_stretch = True
        self.api = SeeShellScreen.api

    def on_press(self):
        '''
        method that is added to the image widgets to change the color of the
        widget when clicked
        '''
        # toggles the 'selected' attribute
        self.selected = not self.selected
        if self.selected:
            animation = Animation(color=(1, 0, 0, 1), duration=0.25)
            animation.start(self)
        else:
            animation = Animation(color=(1, 1, 1, 1), duration=0.25)
            animation.start(self)


class PhotoAlbum(SeeShellScreen):
    images = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        api = SeeShellScreen.api

    def load_photos(self):
        print('called')
        path_list = []
        directory_path = 'Photos'
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path,filename)
            if os.path.isfile(file_path):
                path_list.append(file_path)

        for filepath in path_list:
            wimg = Image(source=filepath)
            self.add_widget(wimg)

    def delete_image(self):
        selected_widgets = [widget for widget in self.images if widget.selected]
        for widget in selected_widgets:
            self.remove_widget(widget)
            self.images.remove(widget)