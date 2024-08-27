import sqlite3
import json
from datetime import datetime

def create_post(post):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()


        db_cursor.execute("""
            Insert into Posts (user_id, category_id, title, publication_date, image_url, content, approved) values (?,?,?,?,?,?,?)
        """,(
            post['user_id'],
            post['category_id'],
            post['title'],
            datetime.now(),
            post['image_url'],
            post['content'],
            post['approved']
        ))

        id = db_cursor.lastrowid

        return {
            'token': id
        }