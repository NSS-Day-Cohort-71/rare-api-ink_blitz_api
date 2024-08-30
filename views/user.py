import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user or an error message
    """
    if (
        not user.get("first_name")
        or not user.get("last_name")
        or not user.get("username")
        or not user.get("email")
    ):
        return {"error": "All fields are required"}, 400

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid

        return {"token": id, "valid": True}


def get_all_users():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
        id,
        u.first_name,
        u.last_name,
        u.username
        FROM Users u
    """
        )
        query_results = db_cursor.fetchall()
        users = []

        for row in query_results:
            user = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "username": row["username"],
            }
            users.append(user)

        serialized_users = json.dumps(users)
        return serialized_users


def retrieve_user(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """SELECT
        u.id,
        u.first_name,
        u.last_name,
        u.profile_image_url,
        u.email,
        u.username,
        u.created_on
        FROM Users u
        WHERE u.id = ?
    """,
            (pk,),
        )
    query_results = db_cursor.fetchone()
    serialized_user = json.dumps(dict(query_results))

    return serialized_user
