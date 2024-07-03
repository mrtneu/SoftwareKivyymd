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
from kivymd.uix.card import MDCard
from kivy.uix.image import AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.core.image import Image as CoreImage
from kivymd.toast import toast
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
    def __init__(self, **kwargs):
        super(Segunda, self).__init__(**kwargs)
        self.image_bytes = None  # Initialize image bytes
    def select_image(self):
        from plyer import filechooser
        file_path = filechooser.open_file(title="Seleccione una imagen", filters=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.ids.imagen_input.source = file_path[0]
            with open(file_path[0], 'rb') as img_file:
                self.image_bytes = img_file.read()

    def load_estampilla(self, estampilla):
        self.ids.nombre_input.text = estampilla.nombre
        self.ids.año_input.text = str(estampilla.año)
        self.ids.país_input.text = estampilla.país
        self.ids.descripción_input.text = estampilla.descripción
        self.current_id = estampilla.id  # Store current id for update
        # Load image from binary
        image_data = BytesIO(estampilla.imagenb)
        pil_image = PILImage.open(image_data)
        pil_image.save('temp.png')  # Temporarily save the image to load it in Kivy
        self.ids.imagen_input.source = 'temp.png'

    def guardar_cambios(self):
        if not (self.ids.nombre_input.text and self.ids.año_input.text and self.ids.país_input.text and self.ids.descripción_input.text and self.image_bytes):
            toast("Todos los campos deben estar llenos", duration=3)
            return

        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            estampilla = session.query(Estampilla).get(self.current_id)
            estampilla.nombre = self.ids.nombre_input.text
            estampilla.año = int(self.ids.año_input.text)
            estampilla.país = self.ids.país_input.text
            estampilla.descripción = self.ids.descripción_input.text
            estampilla.imagenb = self.image_bytes  # Update image bytes in database
            session.commit()
            toast("Cambios guardados correctamente.", duration=3)
        except Exception as e:
            toast(f"Error al guardar cambios: {str(e)}", duration=3)
            session.rollback()
        finally:
            session.close()


class Tercera(Screen):
    def on_enter(self):
        self.cargar_datos()

    def cargar_datos(self):
        self.ids.estampillas_layout.clear_widgets()  # Clear previous items
        Session = sessionmaker(bind=engine)
        session = Session()
        estampillas = session.query(Estampilla).all()

        for estampilla in estampillas:
            image_data = BytesIO(estampilla.imagenb)
            pil_image = PILImage.open(image_data)
            buffer = BytesIO()
            pil_image.save(buffer, format='PNG')
            buffer.seek(0)
            image_texture = CoreImage(buffer, ext='png').texture

            card = MDCard(size_hint=(.5, .3), spacing=10)
            card.bind(on_release=lambda widget, est=estampilla: self.select_estampilla(est))

            box = MDBoxLayout(orientation='vertical', padding='10dp', spacing=10)
            img = Image(texture=image_texture)
            nombre_label = MDLabel(text=estampilla.nombre, size_hint_y=.2, font_style='H6')
            año_label = MDLabel(text=str(estampilla.año), size_hint_y=.2, font_size='15dp')
            pais_label = MDLabel(text=estampilla.país, size_hint_y=.2, font_size='15dp')

            box.add_widget(img)
            box.add_widget(nombre_label)
            box.add_widget(año_label)
            box.add_widget(pais_label)
            card.add_widget(box)
            self.ids.estampillas_layout.add_widget(card)

        session.close()

    def select_estampilla(self, estampilla):
        app = MDApp.get_running_app()
        app.root.get_screen('2').load_estampilla(estampilla)
        self.manager.current = '2'


    
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
    
    from kivymd.toast import toast
    def guardar_datos(self):
        try:
            nombre = self.root.get_screen('1').ids.Nombre.text.strip()
            año = self.root.get_screen('1').ids.Año.text.strip()
            país = self.root.get_screen('1').ids.País.text.strip()
            descripción = self.root.get_screen('1').ids.Descripción.text.strip()
            imagen_bytes = self.root.get_screen('1').image_bytes

        # Validar que todos los campos requeridos estén llenos
            if not (nombre and año and país and descripción and imagen_bytes):
                toast("Todos los campos deben estar llenos", duration=3)
                return

        # Convertir el año a entero
            año = int(año)

        # Crea una instancia del modelo Estampilla
            nueva_estampilla = Estampilla(nombre=nombre, año=año, país=país, descripción=descripción, imagenb=imagen_bytes)

        # Crea una sesión de SQLAlchemy
            Session = sessionmaker(bind=engine)
            session = Session()

        # Agrega la nueva estampilla a la sesión y confirma los cambios en la base de datos
            session.add(nueva_estampilla)
            session.commit()
            toast("Datos guardados correctamente en la base de datos.", duration=3)
        except ValueError as ve:
            toast(f"Error de validación: {str(ve)}", duration=3)
        except Exception as e:
            toast(f"Error al guardar datos en la base de datos: {str(e)}", duration=3)
            if 'session' in locals():
                session.rollback()
        finally:
            if 'session' in locals():
                session.close()



    
    
    
    

if __name__ == '__main__':
    App().run()
