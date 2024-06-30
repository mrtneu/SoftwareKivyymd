from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.screenmanager import ScreenManager,Screen

class Primera(Screen):
    pass

class Segunda(Screen):
    pass
class Tercera(Screen):
    pass

sm = ScreenManager()
sm.add_widget(Primera(name='1'))
sm.add_widget(Segunda(name='2'))
sm.add_widget(Tercera(name='3'))


class App(MDApp):
    def build(self):

        
        return Builder.load_file('main.kv')


App().run()
