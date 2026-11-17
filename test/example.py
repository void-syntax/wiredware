import sqlite3


def get_user(username: str):
    conn = sqlite3.connect("users.db")
    # Уязвимость: прямая подстановка пользовательского ввода в SQL-запрос
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return conn.execute(query).fetchall()
