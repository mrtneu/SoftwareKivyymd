from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from sqlalchemy import create_engine, text
import sqlalchemy as sa

server = '34.176.110.254'
database = 'ESTAMPILLA'
username = 'sqlserver'
password = 'admin'

connection_string = f'mssql+pymssql://{username}:{password}@{server}/{database}'

engine = create_engine(connection_string)





class Primera(Screen):
    pass

class Segunda(Screen):
    pass


class Tercera(Screen):
    def on_enter(self):
        self.populate_list()

    def populate_list(self):
        query = "SELECT * FROM Estampillas"  # Cambia 'estampillas' por el nombre de tu tabla
        with engine.connect() as connection:
            result = connection.execute(text(query))
            self.ids.lista.clear_widgets()

            for row in result:
                item_text = ' | '.join([str(value) for value in row])
                self.ids.lista.add_widget(OneLineListItem(text=item_text))
    


class App(MDApp):
    def build(self):
        sm = ScreenManager()  # Create ScreenManager here
        sm.add_widget(Primera(name='1'))
        sm.add_widget(Segunda(name='2'))
        sm.add_widget(Tercera(name='3'))

        return Builder.load_file('main.kv')
       
    

if __name__ == '__main__':
    App().run()
