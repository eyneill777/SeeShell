from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import  Screen
import os
from kivy.uix.screenmanager import ScreenManager, Screen


class SelectableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SelectableImage, self).__init__(**kwargs)
        self.allow_stretch = True

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


class PhotoAlbum(Screen):
    #images = ListProperty([])

    def __init__(self, manager,api, **kwargs):
        Builder.load_file('gallery.kv')
        self.manager = manager
        #self.screen_manager = manager
        super(PhotoAlbum, self).__init__(**kwargs)
        self.on_enter()
        self.cols = 3
        #self.spacing = 10
        self.api = api
        self.on_enter()


    def on_enter(self):
        print('called')
        photo_list = []
        directory_path = 'Photos'
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path,filename)
            if os.path.isfile(file_path):
                photo_list.append(file_path)

        for i in photo_list:
            wimg = Image(source = i)
            self.add_widget(wimg)

    def go_to_camera_screen(self):
       self.manager.current = 'capture_screen'

    def delete_image(self):
        selected_widgets = [widget for widget in self.images if widget.selected]
        for widget in selected_widgets:
            self.remove_widget(widget)
            self.images.remove(widget)
