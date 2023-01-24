import sqlite3
from models import Snake

def get_all_snakes(query_params):
    """Getter function for species"""
    with sqlite3.connect("./book-2.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        where_clause = ""

        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "species":
                if qs_value != "2":
                    where_clause = f"WHERE species_id = {qs_value}"
                else:
                    return {"message": "Not Allowed"}
        
        sql_string = f"""
        SELECT
            *
        FROM Snakes
        {where_clause}
        """

        db_cursor.execute(sql_string)
        dataset = db_cursor.fetchall()
        snakes = []
        for row in dataset:
            snake = Snake(row["id"], row["name"], row["owner_id"], row["species_id"], row["gender"], row["color"])
            snakes.append(snake.__dict__)
        return snakes

def get_single_snake(id):
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
            species = Snake(data["id"], data["name"], data["owner_id"], data["species_id"], data["gender"], data["color"])
            return species.__dict__

def create_snake(new_snake):
    """Post snake to api with INSERT SQL, add id before returning post to client."""
    with sqlite3.connect('./book-2.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO snakes
            (name, owner_id, species_id, gender, color)
        VALUES (?,?,?,?,?);
        """, (new_snake["name"], new_snake["owner_id"], new_snake["species_id"], new_snake["gender"], new_snake["color"]))

        id = db_cursor.lastrowid

        new_snake["id"] = id

        return new_snake