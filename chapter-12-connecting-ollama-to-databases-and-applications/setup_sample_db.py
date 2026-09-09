# setup_sample_db.py
# Creates a small sample SQLite database for the build-along.

import sqlite3

def setup():
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS orders;

    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        order_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    );

    INSERT INTO customers (name, city) VALUES
        ('Alice Chen', 'Seattle'),
        ('Bob Martinez', 'Austin'),
        ('Carla Diaz', 'Seattle');

    INSERT INTO orders (customer_id, amount, order_date) VALUES
        (1, 129.99, '2026-01-15'),
        (1, 45.50, '2026-02-02'),
        (2, 899.00, '2026-01-20'),
        (3, 210.75, '2026-02-10');
    """)

    conn.commit()
    conn.close()
    print("Sample database created: sample.db")


if __name__ == "__main__":
    setup()
python setup_sample_db.py
