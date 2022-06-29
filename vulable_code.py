from random import randint
import sqlite3
from sqlite3 import Error
import numpy as np


class DataBase:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.connection()

    def __enter__(self):
        return self

    def connection(self):
        try:
            self._conn = sqlite3.connect(self.filename)
        except Error as e:
            print(e)

    def sql(self, query: str, value: tuple = None):
        if value is not None:
            self._conn.cursor()
            self._conn.execute(query, value)
            self._conn.commit()
            return self._conn
        else:
            return self._conn.execute(query)

    def __exit__(self, ext_type, exc_value, traceback):
        self._conn.close()


with DataBase("test.db") as db:
    db.sql(
        """
    CREATE TABLE IF NOT EXISTS contacts
    (
        [id] INTEGER PRIMARY KEY,
        [name] TEXT,
        [age] INTEGER
    )
    """
    )
    enter = int(
        input(
            """
    Type 1 to enter contact 
    Type 2 to search for contact by name 
    Type 3 to Delete user 
    """
        )
    )
    if enter == 1:
        name = str(input("Your Name contact into list "))
        age = int(input("Enter your age "))
        id = randint(0, 100)
        d = np.random.random_integers(0, 100)
        db.sql(
            f"""INSERT INTO  contacts (id, name, age) VALUES (?,?,?);""",
            (id, name, age),
        )
    if enter == 2:
        search = input("Find user ")
        for i in db.sql(f"SELECT * FROM contacts WHERE name = '{search}';"):
            print(i)

    if enter == 3:
        search = input("Find user ")
        db.sql(f"DELETE FROM contacts WHERE name = '{search}';")
        print(f"Deleted {search}")
