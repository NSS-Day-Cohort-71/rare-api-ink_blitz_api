import sqlite3
import json


def create_comment(comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Comments (post_id, author_id, content) VALUES (?,?,?)
        """,
            (comment["post_id"], comment["author_id"], comment["content"]),
        )

        new_comment_id = db_cursor.lastrowid

        return new_comment_id


def list_comments():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content,
            u.username
        FROM Comments c
        JOIN Users u ON u.id = c.author_id
        ORDER BY c.id ASC
        """
        )
        query_results = db_cursor.fetchall()

        comments = []
        for row in query_results:
            comments.append(dict(row))

        serialized_posts = json.dumps(comments)

    return serialized_posts

def update_comment(pk, comment_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """UPDATE Comments
        SET
            content = ?
        WHERE id = ?
    """,
            (comment_data["content"], pk),
        )

        rows_affected = db_cursor.rowcount
    return True if rows_affected > 0 else False