import sqlite3
import json
from datetime import datetime


def create_post(post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            Insert into Posts (user_id, category_id, title, publication_date, image_url, content, approved) values (?,?,?,?,?,?,True)
        """,
            (
                post["user_id"],
                post["category_id"],
                post["title"],
                datetime.now(),
                post["image_url"],
                post["content"],
            ),
        )

        new_post_id = db_cursor.lastrowid

        return new_post_id


def retrieve_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.username
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        WHERE p.id = ?
        """,
            (pk,),
        )
        query_results = db_cursor.fetchone()

        serialized_post = json.dumps(dict(query_results))

    return serialized_post
