import sqlite3


def get_user(username):
    conn = sqlite3.connect("users.db")
    # VULNERABILITY: SQL INJECTION
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return conn.execute(query).fetchone()
