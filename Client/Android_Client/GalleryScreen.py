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

    def __init__(self, id, ext, screen, **kwargs):
        super(SelectableImage, self).__init__(**kwargs)
        self.allow_stretch = True
        self.api = SeeShellScreen.api
        self.id = id
        self.ext = ext
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
            blurbScreen.target = self.id + self.ext
            self.screen.manager.transition.direction = 'up'
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
                                               pos_hint={"center_x": .5, "center_y": .13}, size_hint=(.8,.07),
                                               text_color=(79/255, 193/255, 233/255, 1), on_press=self.cancel)

    def cancel(self,button):
        '''
        Cancels delete
        '''
        self.remove_widget(button)
        self.ids.instruction.color = 0,0,0,1
        self.ids.delete_button.text = "SELECT IMAGES"
        self.ids['delete_button'].text_color = 79/255, 193/255, 233/255, 1
        self.selecting = not self.selecting
    def delete_image(self):
        '''
        Removes image and identification from device
        '''
        if self.selecting:
            self.remove_widget(self.cancel_widget)
            self.selecting = not self.selecting
            selected_widgets = [widget for widget in self.ids.ImageLayout.children if widget.selected]
            for widget in selected_widgets:
                id = widget.id
                self.ids.ImageLayout.remove_widget(widget)
                for extension in [".png", ".json", ".jpg", ".PNG", ".JSON", ".JPG", ".jpeg", ".JPEG"]:
                    file_path = os.path.join(self.directory_path, id + extension)
                    try:
                        os.remove(file_path)
                    except:
                        pass
            self.clean_up_jsons()
            self.ids.delete_button.text = "SELECT IMAGES"
            self.ids.instruction.color = 0,0,0,1
            self.ids['delete_button'].text_color = 79 / 255, 193 / 255, 233 / 255, 1
        else:
            self.selecting = not self.selecting
            self.ids.delete_button.text = "DELETE IMAGES"
            self.ids.instruction.color = 1,1,1,0
            self.ids['delete_button'].text_color = 1, 0, 0, 1
            self.add_widget(self.cancel_widget)

    def clean_up_jsons(self):
        '''
        removes json files that have been left hanging (when an image is deleted before classified, and the message is recieved after)
        '''
        ids_to_delete = []
        photos_folder = os.listdir(self.directory_path)
        for filename in photos_folder:
            id,ext = filename.split('.')[0],filename.split('.')[1]
            if ext == 'json':
                ids_to_delete.append(id)
        for filename in photos_folder:
            id, ext = filename.split('.')[0], filename.split('.')[1]
            if ext != 'json':
                try:
                    ids_to_delete.remove(id)
                except ValueError:
                    pass
        for id in ids_to_delete:
            filepath = os.path.join(self.directory_path, id + '.json')
            os.remove(filepath)

    def load_photos(self):
        '''
        Loads captured and uploaded photos into scrollable gallery view
        '''
        print('loading photos')
        self.ids.ImageLayout.clear_widgets()
        
        paths = {}
        for filename in os.listdir(self.directory_path):
            file_path = os.path.join(self.directory_path, filename)
            if os.path.isfile(file_path):
                if file_path.split('.')[1] != 'json' and file_path.split('.')[1] != 'DS_Store':
                    paths[filename] = file_path
        for file in paths:
            uuid = file.split('.')[0]
            ext = '.'+file.split('.')[1]
            wimg = SelectableImage(size = ((self.get_parent_window().width),(self.get_parent_window().width/2.7)),pos =(self.x - 10, self.y - 10),
                                   source=paths[file], id= uuid, ext=ext, screen=self, size_hint_y=None)
            self.ids.ImageLayout.add_widget(wimg)
        if len(paths) == 1:
            filepath = os.path.join('assets', 'blank.png')
            self.ids.ImageLayout.add_widget(Image(source=filepath))
