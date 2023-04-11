import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.properties import BooleanProperty


class SelectableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SelectableImage, self).__init__(**kwargs)
        self.allow_stretch = True

    def on_press(self):
        self.selected = not self.selected
        if self.selected:
            animation = Animation(color=(1, 0, 0, 1), duration=0.25)
            animation.start(self)
        else:
            animation = Animation(color=(1, 1, 1, 1), duration=0.25)
            animation.start(self)


class PhotoAlbum(GridLayout):
    images = ListProperty([])

    def __init__(self, **kwargs):
        super(PhotoAlbum, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 10

        # create the 'Add Image' button
        # self.add_widget(Button(text='Add Image', on_press=self.add_image))

        self.upload_button = Button(text='Add Image', size_hint=(None, None), size=(200, 50))
        self.upload_button.bind(on_press=self.add_image)

        self.delete_button = Button(text='Delete', size_hint=(None, None), size=(200, 50))
        self.delete_button.bind(on_press=self.delete_image)

        self.camera_btn = Button(text='Camera', size_hint=(None, None), size=(200, 50))
        self.camera_btn.bind(on_release=self.camera_screen)

        self.add_widget(self.upload_button)
        self.add_widget(self.delete_button)
        self.add_widget(self.camera_btn)
        # Add buttons to the bottom of the screen

    def camera_screen(self, instance):
        from capturemode import TestCamera
        TestCamera().run()

    def add_image(self, *args):
        # open a file selection dialog and get the selected file
        from kivy.uix.filechooser import FileChooserIconView
        chooser = FileChooserIconView()
        chooser.path = os.path.expanduser('~')
        chooser.filters = ['*.png', '*.jpg', '*.jpeg']
        chooser.bind(selection=self.load_image)
        popup = BoxLayout()
        popup.add_widget(chooser)
        App.get_running_app().root_window.add_widget(popup)

    def load_image(self, chooser, selection):
        if selection:
            # create a new selectable image widget and add it to the album
            img = SelectableImage(source=selection[0], allow_stretch=True)
            self.images.append(img)
            self.add_widget(img)
        chooser.parent.parent.remove_widget(chooser.parent)

    def delete_image(self, instance):
        selected_widgets = [widget for widget in self.images if widget.selected]
        for widget in selected_widgets:
            self.remove_widget(widget)
            self.images.remove(widget)



class GalleryApp(App):
    def build(self):
        return PhotoAlbum()


if __name__ == '__main__':
    GalleryApp().run()