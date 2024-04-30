import sqlite3 as sq


def main(db_path: str):
    # Connect to the database (creating it if it doesn't exist)
    with sq.connect(db_path) as con:
        # Create a cursor object to execute SQL commands
        cur = con.cursor()

        # Drop the tables if they already exist
        cur.execute("DROP TABLE IF EXISTS orders")
        cur.execute("DROP TABLE IF EXISTS feedback_records")

        # Create the 'orders' table if it doesn't exist
        cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        phone TEXT NOT NULL,
        city TEXT NOT NULL,
        model TEXT NOT NULL,
        watch_id INTEGER NOT NULL
        )""")

        # Create the 'feedback_records' table if it doesn't exist
        cur.execute("""CREATE TABLE IF NOT EXISTS feedback_records(
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        feedback_text TEXT NOT NULL,
        feedback_sentiment TEXT NOT NULL
        )""")


if __name__ == "__main__":
    main(db_path="../database.db")
