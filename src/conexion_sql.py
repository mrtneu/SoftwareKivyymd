from sqlalchemy import create_engine, text


server = 'PC\\SQLEXPRESS'
database = 'ESTAMPILLAS'
driver = 'ODBC Driver 17 for SQL Server'

connection_string = f'mssql+pyodbc://@{server}/{database}?driver={driver}&trusted_connection=yes'

engine = create_engine(connection_string)


with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM Estampillas"))
    for row in result:
        print(row)