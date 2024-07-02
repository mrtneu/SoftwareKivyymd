from sqlalchemy import create_engine, text


server = '34.176.110.254'
database = 'ESTAMPILLA'
username = 'sqlserver'
password = 'admin'

#Conexion
connection_string = f'mssql+pymssql://{username}:{password}@{server}/{database}'

engine = create_engine(connection_string)

