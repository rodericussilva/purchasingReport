import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={SQL Server};'
        f'SERVER={os.getenv("DB_SERVER")};'
        f'DATABASE={os.getenv("DB_DATABASE")};'
        f'UID={os.getenv("DB_UID")};'
        f'PWD={os.getenv("DB_PWD")}'
    )
    return connection