#!/usr/bin/env python3
import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator to automatically handle DB connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """Decorator to cache query results based on SQL string"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get query from kwargs or args
        query = kwargs.get("query", args[0] if args else None)
        if query in query_cache:
            print(f"[CACHE] Returning cached result for query: {query}")
            return query_cache[query]

        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE] Stored result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    # First call will execute and cache
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
