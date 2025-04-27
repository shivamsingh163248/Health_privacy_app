import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,  # <--- Pass the port separately
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

