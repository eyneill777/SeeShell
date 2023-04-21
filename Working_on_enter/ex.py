from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

KV = """
<Screen1>:
    Button:
        text: "Go to Screen 2"
        on_press: root.manager.current = "screen2"

<Screen2>:
    Button:
        text: "Go to Screen 1"
        on_press: root.manager.current = "screen1"

Manager:
    Screen1:
        name: "screen1"

    Screen2:
        name: "screen2"
"""


class Manager(ScreenManager):
    pass


class Screen1(Screen):
    def on_enter(self):
        print("Enter screen 1")


class Screen2(Screen):
    def on_enter(self):
        print("Enter screen 2")


class MyApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    MyApp().run()
