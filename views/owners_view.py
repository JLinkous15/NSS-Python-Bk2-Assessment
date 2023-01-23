import sqlite3
from models import Owner

def get_all_owners():
    with sqlite3.connect("./book-2.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT *
        FROM Owners
        """)
        dataset = db_cursor.fetchall()
        owners = []
        for row in dataset:
            owner = Owner(row["id"], row["first_name"], row["last_name"], row["email"])
            owners.append(owner.__dict__)
        return owners

def get_single_owner(id):
    with sqlite3.connect("./book-2.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT *
        FROM Owners
        WHERE id = ?
        """, (id,))
        data = db_cursor.fetchone()
        owner = Owner(data["id"], data["first_name"], data["last_name"], data["email"])
        return owner.__dict__