#!/usr/bin/python3
"""
Generator function that streams rows from user_data table one by one.
"""

import mysql.connector


def stream_users():
    """
    Connects to ALX_prodev database and yields rows from user_data table.
    Each row is returned as a dictionary.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # update if different
            password="password",  # update with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return
