from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivymd.uix.button import MDRoundFlatButton
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
        if self.screen.selecting:
            self.selected = not self.selected
            if self.selected:
                animation = Animation(color=(.6, 1, .6, 1), duration=0.25)
                animation.start(self)
            else:
                animation = Animation(color=(1, 1, 1, 1), duration=0.25)
                animation.start(self)
        else:
            blurbScreen.target = self.id
            self.screen.manager.current = "blurb_screen"


        # toggles the 'selected' attribute


                
class PhotoAlbum(SeeShellScreen):
    
    def on_pre_enter(self, *args):
        self.load_photos()
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = SeeShellScreen.api
        self.directory_path = 'Photos'
        self.selecting = False
        self.cancel_widget = MDRoundFlatButton(text="Cancel", font_name="assets/poppins/Poppins-SemiBold.ttf",
                                               pos_hint={"center_x": .7, "center_y": .9}, size_hint=(.8,.07),
                                               text_color=(79/255, 193/255, 233/255, 1), on_press=self.change_selecting)

    def change_selecting(self,button):
        self.remove_widget(button)
        self.selecting = not self.selecting
    def delete_image(self):
        if self.selecting:
            self.remove_widget(self.cancel_widget)
            self.selecting = not self.selecting
            selected_widgets = [widget for widget in self.ids.ImageLayout.children if widget.selected]
            for widget in selected_widgets:
                id = widget.id
                self.ids.ImageLayout.remove_widget(widget)
                for extension in [".png", ".json", "jpg"]:
                    file_path = os.path.join(self.directory_path, id + extension)
                    try:
                        os.remove(file_path)
                    except:
                        pass
            self.ids.delete_button.text = "SELECT IMAGES"
        else:
            self.selecting = not self.selecting
            self.ids.delete_button.text = "DELETE IMAGES"
            self.add_widget(self.cancel_widget)

            
            
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
