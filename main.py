from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem, ThreeLineListItem, IconRightWidget,OneLineAvatarListItem, ImageLeftWidget
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from sqlalchemy import create_engine, text, MetaData, Table, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text
from kivy.utils import platform
from kivy.uix.filechooser import FileChooserIconView
import os,shutil
import sqlalchemy as sa


server = '34.176.110.254'
database = 'ESTAMPILLA'
username = 'sqlserver'
password = 'admin'

connection_string = f'mssql+pymssql://{username}:{password}@{server}/{database}'

engine = create_engine(connection_string)

Base = declarative_base()

# Define tu modelo SQLAlchemy
class Estampilla(Base):
    __tablename__ = 'Estampillas'  # Nombre de tu tabla en la base de datos
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    año = Column(Integer)
    país = Column(String)
    descripción = Column(Text)
    imagen = Column(String)


class Primera(Screen):
    def select_file(self):
        from plyer import filechooser
        filechooser.open_file(on_selection = self.selected)

    def selected(self, selection):
        if selection:
            src = selection[0]
            dst = "C:/Users/ishie/OneDrive/Documentos/GitHub/SoftwareKivyymd/img"
            final = shutil.copy2(src,dst)
            print(final) 
            self.ids.Imagen_texto.text = final
            self.ids.Imagen.source = src


class Segunda(Screen):
    pass



class Tercera(Screen):
    def on_enter(self):
        self.populate_list()

    def populate_list(self):
        inspector = inspect(engine)
        columns = inspector.get_columns('estampillas')
        column_titles = '   |   '.join([col['name'] for col in columns])
        self.ids.lista.clear_widgets()
        self.ids.lista.add_widget(OneLineListItem(text=column_titles, bg_color=(0.8, 0.8, 0.8, 1)))  # Color de fondo para diferenciar

        query = "SELECT * FROM Estampillas"  # Cambia 'estampillas' por el nombre de tu tabla
        with engine.connect() as connection:
            result = connection.execute(text(query))
            for row in result:
                item_text = '   |   '.join([str(value) for value in row])
                self.ids.lista.add_widget(OneLineListItem(text=item_text))
    
    
class Cuarta(Screen):
    pass

class App(MDApp):
    def build(self):
        sm = ScreenManager()  # Create ScreenManager here
        sm.add_widget(Primera(name='1'))
        sm.add_widget(Segunda(name='2'))
        sm.add_widget(Tercera(name='3'))
        sm.add_widget(Cuarta(name='4'))
        return Builder.load_file('main.kv')
    
    def guardar_datos(self):
        nombre = self.root.get_screen('1').ids.Nombre.text
        año = int(self.root.get_screen('1').ids.Año.text)
        país = self.root.get_screen('1').ids.País.text
        descripción = self.root.get_screen('1').ids.Descripción.text
        imagen = self.root.get_screen('1').ids.Imagen_texto.text

        # Crea una instancia del modelo Estampilla
        nueva_estampilla = Estampilla(nombre=nombre, año=año, país=país, descripción=descripción, imagen=imagen)

        # Crea una sesión de SQLAlchemy
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Agrega la nueva estampilla a la sesión y confirma los cambios en la base de datos
            session.add(nueva_estampilla)
            session.commit()
            print("Datos guardados correctamente en la base de datos.")
        except Exception as e:
            print(f"Error al guardar datos en la base de datos: {str(e)}")
            session.rollback()
        finally:
            session.close()

    
    
    
    

if __name__ == '__main__':
    App().run()
