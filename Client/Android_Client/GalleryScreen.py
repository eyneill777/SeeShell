from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.lang import Builder


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


class PhotoAlbum(GridLayout):
    images = ListProperty([])
    Builder.load_file('gallery.kv')
    def __init__(self, manager,api, **kwargs):
        self.manager = manager
        self.screen_manager = manager
        super(PhotoAlbum, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 10
        self.api = api

    def go_to_camera_screen(self, instance):
       self.screen_manager.current = 'capture_screen'

    def delete_image(self, instance):
        selected_widgets = [widget for widget in self.images if widget.selected]
        for widget in selected_widgets:
            self.remove_widget(widget)
            self.images.remove(widget)
