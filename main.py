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
from sqlalchemy import Column, Integer, String, Text, LargeBinary
from kivy.utils import platform
from kivy.uix.filechooser import FileChooserIconView
from io import BytesIO
from PIL import Image as PILImage 
from kivy.uix.image import AsyncImage
from kivy.core.image import Image as CoreImage
import os,shutil
import sqlalchemy as sa
import base64

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
    imagenb = Column(LargeBinary)


class Primera(Screen):
    def select_file(self):
        from plyer import filechooser
        filechooser.open_file(on_selection = self.selected)

    def selected(self, selection):
        if selection:
            src = selection[0]
            with open(src, 'rb') as f:
                image_bytes = f.read()
            
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')            
            self.ids.Imagen_texto.text = image_base64
            self.image_bytes = image_bytes

            self.ids.Imagen.source = src


class Segunda(Screen):
    pass



class Tercera(Screen):
    def on_enter(self):
        self.populate_list()

    def populate_list(self):
        inspector = inspect(engine)
        columns = inspector.get_columns('Estampillas')
        column_names = [col['name'] for col in columns]

        query = "SELECT * FROM Estampillas"
        with engine.connect() as connection:
            result = connection.execute(text(query))

            for row in result:
                item_widget = OneLineAvatarListItem()

                item_text = ''
                for idx, col_name in enumerate(column_names):
                    if col_name != 'ImagenB':
                        if idx > 0:
                            item_text += ' | '
                        item_text += str(row[idx])

                item_widget.text = item_text

                # Mostrar la imagen si hay datos de imagen binaria
                imagen_index = column_names.index('ImagenB')
                if row[imagen_index]:
                    # Convertir los bytes de la imagen a una imagen que Pillow pueda manejar
                    imagen_bytes = row[imagen_index]
                    image_pil = PILImage.open(BytesIO(imagen_bytes))
                    
                    # Redimensionar la imagen para generar una miniatura
                    thumbnail_size = (100, 100)  # Tamaño de la miniatura deseado
                    image_pil.thumbnail(thumbnail_size)

                    # Convertir la imagen de Pillow a un formato que Kivy pueda usar
                    buffer = BytesIO()
                    image_pil.save(buffer, format='png')
                    buffer.seek(0)

                    # Crear un widget de imagen y establecer la miniatura desde el buffer
                    image_texture = CoreImage(buffer, ext='png').texture
                    image_widget = AsyncImage(texture=image_texture)

                    # Agregar la imagen al ítem de la lista
                    item_widget.add_widget(image_widget)

                # Agregar el widget a la lista
                self.ids.lista.add_widget(item_widget)
    
    
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
        imagen_bytes = self.root.get_screen('1').image_bytes

        # Crea una instancia del modelo Estampilla
        nueva_estampilla = Estampilla(nombre=nombre, año=año, país=país, descripción=descripción, imagenb=imagen_bytes)

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
