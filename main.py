from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window




class App(MDApp):
    def build(self):

       
        return Builder.load_file('main.kv')

    def callback(self):
        pass

    def load_image(self):
        image_path = self.root.ids.image_path.text
        self.root.ids.image.source = image_path

App().run()
