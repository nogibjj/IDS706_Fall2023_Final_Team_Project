# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World!"}

from fastapi import FastAPI
import pyodbc

app = FastAPI()

# Connection string
conn_str = (
    r'Driver={ODBC Driver 18 for SQL Server};'
    r'Server=tcp:ids706-final-sql-server.database.windows.net,1433;'
    r'Database=ids706-final-sql;'
    r'Uid=ids706-final;'
    r'Pwd={P0stgres};'
    r'Encrypt=yes;'
    r'TrustServerCertificate=no;'
    r'Connection Timeout=30;'
)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/data")
async def get_data():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dbo.application_data_test')  # replace 'your_table' with your actual table name
    rows = cursor.fetchall()
    return {"data": [dict(zip([column[0] for column in cursor.description], row)) for row in rows]}