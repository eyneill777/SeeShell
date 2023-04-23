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

        blurbScreen.target = self.id

        # toggles the 'selected' attribute
        self.selected = not self.selected
        if self.selected:
            animation = Animation(color=(.6, 1, .6, 1), duration=0.25)
            animation.start(self)
        else:
            animation = Animation(color=(1, 1, 1, 1), duration=0.25)
            animation.start(self)

                
class PhotoAlbum(SeeShellScreen):
    
    def on_pre_enter(self, *args):
        self.load_photos()
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api
        self.directory_path = 'Photos'

    def delete_image(self):
        selected_widgets = [widget for widget in self.ids.ImageLayout.children if widget.selected]
        for widget in selected_widgets:
            self.ids.ImageLayout.remove_widget(widget)
            id = (SelectableImage)(widget).id
            for extension in [".png", ".json"]:
                file_path = os.path.join(self.directory_path, id+extension)
                try:
                    os.remove(file_path)
                except:
                    pass
            
            
    def load_photos(self):
        print('loading photos')
        self.ids.ImageLayout.clear_widgets()
        
        paths = {}
        for filename in os.listdir(self.directory_path):
            file_path = os.path.join(self.directory_path, filename)
            if os.path.isfile(file_path):
                if file_path.split('.')[1] != 'json' and file_path.split('.')[1] != 'DS_Store':
                    paths[filename] = file_path
                    print(file_path)

        for file in paths:
            uuid = file.split('.')[0]
            wimg = SelectableImage(source=paths[file], id= uuid, screen=self, size_hint=(None, None))
            self.ids.ImageLayout.add_widget(wimg)
