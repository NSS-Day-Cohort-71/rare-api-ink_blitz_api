import sqlite3
import json
from datetime import datetime


def create_post(post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            Insert into Posts (user_id, category_id, title, publication_date, image_url, content, approved) values (?,?,?,?,?,?,False)
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
            u.username,
            c.label AS category_label
        FROM Posts p
        JOIN Users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.id = ?
        """,
            (pk,),
        )
        query_results = db_cursor.fetchone()

        serialized_post = json.dumps(dict(query_results))

    return serialized_post


def update_post(pk, post_data):

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """UPDATE Posts
        SET 
            title = ?,  
            image_url = ?,
            content = ?,
            category_id = ?
        WHERE id = ?
    """,
            (
                post_data["title"],
                post_data["image_url"],
                post_data["content"],
                post_data["category_id"],
                pk,
            ),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def list_posts():
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
        WHERE p.approved = 1
        ORDER BY p.publication_date DESC                                                                                                                    
        """
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            posts.append(dict(row))

        serialized_posts = json.dumps(posts)

    return serialized_posts


def delete_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Posts WHERE id = ?
    """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
