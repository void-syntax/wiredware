import sqlite3


def get_user(user_id):
    conn = sqlite3.connect("users.db")
    conn.cursor().execute(f"SELECT * FROM users WHERE id = {user_id}")
