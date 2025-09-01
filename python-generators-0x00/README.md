# Python Generators – Task 0

## Objective

Create a generator that streams rows from an SQL database **one by one**.

## Files

* **seed.py** → handles database connection, setup, seeding, and streaming.
* **0-main.py** → entry script to test seeding and querying.
* **user\_data.csv** → sample dataset to populate the table.

## Functions in `seed.py`

### 1. `connect_db()`

Connects to the MySQL server (without specifying a database).

### 2. `create_database(connection)`

Creates the database **ALX\_prodev** if it does not exist.

### 3. `connect_to_prodev()`

Connects directly to the **ALX\_prodev** database.

### 4. `create_table(connection)`

Creates the `user_data` table if it does not exist with fields:

* `user_id` (UUID, Primary Key, Indexed)
* `name` (VARCHAR, NOT NULL)
* `email` (VARCHAR, NOT NULL)
* `age` (DECIMAL, NOT NULL)

### 5. `insert_data(connection, data)`

Inserts data from `user_data.csv` into the database.

### 6. `stream_users(connection)`

A **Python generator** that yields rows from `user_data` **one at a time**.

Example:

```python
from seed import connect_to_prodev, stream_users

conn = connect_to_prodev()
for row in stream_users(conn):
    print(row)
```

## Usage

```bash
# Run seeding script
./0-main.py
```

Expected output (first few lines):

```
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'John Doe', 'john@example.com', 30), ('uuid2', 'Jane Doe', 'jane@example.com', 25), ...]
```

---

⚠️ **Note:** Update your MySQL `user` and `password` inside `seed.py` to match your environment.
