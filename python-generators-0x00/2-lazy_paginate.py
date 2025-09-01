#!/usr/bin/python3
"""
Lazy loading paginated data from user_data table using a generator.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users with a given limit and offset.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users.
    Fetches the next page only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
