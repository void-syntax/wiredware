import sqlite3


def get_user(username):
    conn = sqlite3.connect("users.db")
    # FIX: USE PLACEHOLDER
    query = "SELECT * FROM users WHERE username = ?"
    return conn.execute(query).fetchone()
