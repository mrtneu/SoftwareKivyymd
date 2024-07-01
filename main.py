from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.screenmanager import ScreenManager,Screen
from sqlalchemy import create_engine, text

# Configuración de la conexión
server = '34.176.110.254'
database = 'ESTAMPILLA'
username = 'sqlserver'
password = 'admin'

# Cadena de conexión
connection_string = f'mssql+pymssql://{username}:{password}@{server}/{database}'

# Crear el motor de SQLAlchemy
engine = create_engine(connection_string)

try:
    with engine.connect() as connection:
        # Ejemplo de consulta
        query = "SELECT * FROM Estampillas"  # Aquí colocas tu consulta SQL
        result = connection.execute(text(query))
        
        # Procesar los resultados
        for row in result:
            print(row)

except Exception as e:
    print(f"Error al ejecutar la consulta: {str(e)}")



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
