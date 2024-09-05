import sqlite3
import json


def create_post_tag(post_tag):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    INSERT INTO PostTags (post_id, tag_id) VALUES (?,?)
    """,
            (post_tag["post_id"], post_tag["tag_id"]),
        )
        new_post_tag_id = db_cursor.lastrowid
    return new_post_tag_id


def retrieve_post_tags(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
    SELECT
        pt.id,
        t.id AS tag_id,
        t.label
    
    FROM Tags t
    JOIN PostTags pt ON pt.tag_id = t.id
    WHERE pt.post_id = ?
    """,
            (post_id,),
        )
        query_results = db_cursor.fetchall()
        tags = []
        for row in query_results:
            tags.append(dict(row))

        serialized_post_tags = json.dumps(tags)

    return serialized_post_tags


# def update_post_tags(post_tag_data):
#     with sqlite3.connect("./db.sqlite3") as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         db_cursor.execute(
#             """

#     """
#         )
