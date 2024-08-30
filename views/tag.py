import sqlite3
import json


def create_tag(tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Tags (label) VALUES (?)
        """,
            (tag["label"],),
        )

        new_tag_id = db_cursor.lastrowid

        return new_tag_id


def list_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    SELECT
        t.id,
        t.label
    FROM Tags t
    """
        )
        query_results = db_cursor.fetchall()

        tags = []
        for row in query_results:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)

    return serialized_tags


def retrieve_tag(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    SELECT
        t.id,
        t.label
    FROM Tags t
    WHERE t.id = ?
    """,
            (pk,),
        )
        query_results = db_cursor.fetchone()

        serialized_tag = json.dumps(dict(query_results))

        return serialized_tag


def update_tag(pk, tag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    UPDATE Tags
    SET
        label = ?
    WHERE id = ?
    """,
            (tag_data["label"], pk),
        )
    rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False
