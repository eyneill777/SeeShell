import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from plyer import filechooser
from kivy.uix.floatlayout import FloatLayout


class PhotoAlbum(App):
    def build(self):
        # create the main layout
        main_layout = BoxLayout(orientation='vertical')

        # create a list to store the images
        self.images = []

        # create a button to add images
        add_btn = Button(text='Add Image', size_hint=(None, None), size=(100, 50), pos=(650, 40))
        delete_btn = Button(text='Delete Image', size_hint=(None, None), size=(100, 50), pos=(535, 40))

        add_btn.bind(on_press=self.open_file_chooser)
        delete_btn.bind(on_press=self.delete_widget)


        # add the button to the main layout
        main_layout.add_widget(add_btn)
        main_layout.add_widget(delete_btn)


        return main_layout

    def delete_widget(self, instance):
        # remove the label from the layout
        self.remove_widget(self.widget)


    def open_file_chooser(self, instance):
        # open the file chooser
        filechooser.open_file(on_selection=self.load_image)

    def load_image(self, selection):
        # check if a file was selected
        if selection:
            # create the image widget and add it to the main layout
            image = Image(source=selection[0], size_hint=(1, None))
            self.images.append(image)
            self.root.add_widget(image)
        else:
            # create a popup to inform the user that no file was selected
            popup = Popup(title='Error',
                          content=Label(text='No file selected.'),
                          size_hint=(None, None),
                          size=(Window.width * 0.8, Window.height * 0.2))
            popup.open()


if __name__ == '__main__':
    PhotoAlbum().run()
