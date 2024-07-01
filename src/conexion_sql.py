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