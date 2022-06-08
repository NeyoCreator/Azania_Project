import sqlite3
from sqlite3 import Error


# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()


# if __name__ == '__main__':
#     create_connection(r"C:\Users\NeoSebanze\Desktop\June\2.jabuu\jabuu\3.login_registration\database\database.db")

#EDIT OF DATABASE
from app import db 

db.create_all()