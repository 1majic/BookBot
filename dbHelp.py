import sqlite3
from random import randint


def startDB():
    global conn, cursor
    conn = sqlite3.connect("books/BooksReviews.db")
    cursor = conn.cursor()


def MakeNewTable(tname, *columns):
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tname}(
   {', '.join(columns)});
""")


def AddNewObject(tablename, params):
    cursor.execute(f"INSERT INTO {tablename} VALUES({params});")


def FindByName(tablename, name):
    cursor.execute(f'select * from {tablename} where name = "{name}"')
    return cursor.fetchall()


def FindById(tablename, bookid):
    cursor.execute(f"select * from {tablename} where id = {bookid}")
    return cursor.fetchall()


def LastId(tablename):
    cursor.execute(f"select max (id) from {tablename}")
    maxId = cursor.fetchone()[0]
    cursor.execute(f"select * from {tablename} where id = {randint(1, maxId)}")
    return cursor.fetchone()


if __name__:
    startDB()
