"""
from os import getcwd, path, sep
import sqlite3

def create_connection() -> sqlite3.Connection:
    return sqlite3.connect(database='data.db')

def create_cursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    return connection.cursor()


cursor = create_cursor(connection=create_connection())
"""

def insert_id(id: str):
    pass