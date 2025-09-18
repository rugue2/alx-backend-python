#!/usr/bin/env python3
import sqlite3
import functools

<<<<<<< HEAD
def with_db_connection(func):
    """Decorator to automatically handle DB connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            # inject connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
=======
def with_db_connection(func):
    """Decorator to automatically handle DB connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            # inject connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)

>>>>>>> 49d428595850d1d8342388cb6ca607833c52011b