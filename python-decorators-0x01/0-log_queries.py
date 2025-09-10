#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime   # ✅ required import

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] Executing SQL Query: {query}")
        else:
            print(f"[{datetime.now()}] No SQL query provided")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)