#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for handling DB connections"""

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn   # connection object is returned

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                # Rollback if there was an error
                self.conn.rollback()
            else:
                # Commit changes if all good
                self.conn.commit()
            self.conn.close()
        # Returning False propagates the exception if any occurred
        return False


# Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
