import mysql.connector

from core import settings

dataBase = mysql.connector.connect(
    host = settings.DB_HOST,
    user = settings.DB_USER,
    paswd = settings.DB_PASSWORD,
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a DataBase
cursorObject.execute(f"CREATE DATABASE {settings.DB_NAME}")