import sqlite3


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
