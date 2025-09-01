#!/usr/bin/python3
"""
Batch processing of users using Python generators.
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches users in batches from the user_data table.
    Yields a list of rows (batch).
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # update if needed
            password="password",  # update with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return


def batch_processing(batch_size):
    """
    Processes batches of users, filtering only users with age > 25.
    Yields filtered user dictionaries.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if int(user["age"]) > 25:
                print(user)
                yield user
