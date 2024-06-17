import mysql.connector
from core import settings

def create_database():
    try:
        dataBase = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursorObject = dataBase.cursor()
        cursorObject.execute(f"CREATE DATABASE {settings.DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        if 'dataBase' in locals() and dataBase.is_connected():
            cursorObject.close()
            dataBase.close()
