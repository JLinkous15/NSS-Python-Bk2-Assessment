import sqlite3
from models import Species

def get_all_species():
    """Getter function for species"""
    with sqlite3.connect("./book-2.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sql_string = """
        SELECT *
        FROM species
        """
        db_cursor.execute(sql_string)
        dataset = db_cursor.fetchall()
        all_species = []
        for row in dataset:
            species = Species(row["id"], row["name"])
            all_species.append(species.__dict__)
        return all_species

def get_single_species(id):
    """Getter function for single species by primary key"""
    with sqlite3.connect("./book-2.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        sql_string = """
        SELECT *
        FROM species
        WHERE id = ?
        """
        db_cursor.execute(sql_string, (id,))
        data = db_cursor.fetchone()
        if data is None:
            return {"message":"Bad Request"}
        else:
            species = Species(data["id"], data["name"])
            return species.__dict__