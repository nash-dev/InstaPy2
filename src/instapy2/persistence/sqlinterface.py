from os import getcwd, path, sep
import sqlite3

connection = sqlite3.connect(getcwd() + sep + f'files{sep}data.db')
cursor = connection.cursor()

def create_table():
    cursor.execute('CREATE TABLE liked_media (id TEXT)')

def insert_id(id):
    cursor.execute(f'INSERT INTO liked_media VALUES (\'{id}\')')
    connection.commit()

def show():
    print(cursor.execute('SELECT * FROM liked_media').fetchall())


if cursor.execute('SELECT name FROM sqlite_master WHERE name=\'liked_media\'').fetchone() is None:
    create_table()