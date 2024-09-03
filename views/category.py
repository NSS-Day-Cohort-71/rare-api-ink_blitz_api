import sqlite3
import json


def create_category(category):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Categories (label) VALUES (?)
        """,
            (category["label"],),
        )

        new_category_id = db_cursor.lastrowid

        return new_category_id


def list_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            c.id,
            c.label
        FROM Categories c
        """
        )

        query_results = db_cursor.fetchall()

        categories = []
        for row in query_results:
            categories.append(dict(row))

        serialized_categories = json.dumps(categories)

    return serialized_categories


def delete_category(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
DELETE FROM Categories WHERE id = ?
    """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
