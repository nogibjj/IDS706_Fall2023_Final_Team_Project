import io
import pandas as pd
from azure.storage.blob import BlobServiceClient
import pyodbc
from sqlalchemy import create_engine

# Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=ids706finalstorage;AccountKey=PNPwVMJ4uyUHDt6D8GJyajhq8WQZK0oWQYnbWmqyv1Dm9FR+cNmQ6Apx66GWg8KCSKWLWp5gtc1K+ASteQZd+A==;EndpointSuffix=core.windows.net")
blob_client_application_data = blob_service_client.get_blob_client("container", "application_data_test.csv")
# blob_client_previous_application = blob_service_client.get_blob_client("container", "previous_application.csv")

# Read CSV from Azure Blob Storage into pandas DataFrame
application_data_data = blob_client_application_data.download_blob().readall()
application_df = pd.read_csv(io.BytesIO(application_data_data))

# previous_application_data = blob_client_previous_application.download_blob().readall()
# previous_df = pd.read_csv(io.BytesIO(previous_application_data))

# Azure SQL Database
# server = 'ids706-final-db.database.windows.net'
# database = 'ids706final'
# username = 'your_username'
# password = 'your_password'
# driver= '{ODBC Driver 17 for SQL Server}'

# Connection string
# cnxn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:ids706-final-sql-server.database.windows.net,1433;Database=ids706-final-sql;Uid=ids706-final;Pwd={P0stgres};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
connection_str = "mssql+pyodbc://ids706-final:P0stgres@ids706-final-sql-server.database.windows.net:1433/ids706-final-sql?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(connection_str)

# Write DataFrame to Azure SQL Database
application_df.to_sql('application_data_test', con=connection_str, if_exists='append', index=False)
# previous_df.to_sql('previous_application', con=cnxn, if_exists='append', index=False)