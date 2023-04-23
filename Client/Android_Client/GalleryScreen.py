from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from SeeShellScreen import SeeShellScreen
from BlurbScreen import blurbScreen
import os


class SelectableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)

    def __init__(self, id, screen, **kwargs):
        super(SelectableImage, self).__init__(**kwargs)
        self.allow_stretch = True
        self.api = SeeShellScreen.api
        self.id = id
        self.screen = screen

    def on_press(self):
        '''
        method that is added to the image widgets to change the color of the
        widget when clicked
        '''
        #always true for testing, need to make selecting images to delete possible again later
        if True:
            blurbScreen.target = self.id
            self.screen.manager.current = 'blurb_screen'




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
    
    def on_pre_enter(self, *args):
        self.load_photos()
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api

    def delete_image(self):
        selected_widgets = [widget for widget in self.images if widget.selected]
        for widget in selected_widgets:
            self.remove_widget(widget)
            self.images.remove(widget)

    def load_photos(self):
        print('loading photos')
        path_list = []
        directory_path = 'Photos'
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                if file_path.split('.')[1] != 'json' and file_path.split('.')[1] != 'DS_Store':
                    path_list.append(file_path)
                    print(file_path)


        for filepath in path_list:
            uuid = filepath.split('.')[0][7:]
            wimg = SelectableImage(source=filepath, id= uuid, screen=self, size_hint=(None, None))
            self.ids.ImageLayout.add_widget(wimg)

        if len(path_list) < 3:
            for _ in range(3 - len(path_list)):
                self.ids.ImageLayout.add_widget(Image(source=os.path.join("assets", 'blank.png')))
