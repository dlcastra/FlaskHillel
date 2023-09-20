import sqlite3
from faker import Faker


fake = Faker()


def setup_customers():
    con = sqlite3.connect('flask.db')
    with con as cust_conn:
        cursor = cust_conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(50)
            )"""
        )

        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.company_email()

            cursor.execute(
                """
                INSERT INTO customers (first_name, last_name, email)
                VALUES (?, ?, ?)
                """,
                (first_name, last_name, email)
            )
        cust_conn.commit()


def setup_tracks():
    con = sqlite3.connect('flask.db')
    with con as track_con:
        cursor = track_con.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tracks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_name TEXT,
                track_length INTEGER,
                release_date DATE
            )"""
        )

        for _ in range(100):
            track_name = fake.word()
            track_length = fake.random_int(min=90, max=240)
            release_date = fake.date()

            cursor.execute(
                """
                INSERT INTO tracks (track_name, track_length, release_date)
                VALUES (?, ?, ?)
                """,
                (track_name, track_length, release_date)
            )
        track_con.commit()


setup_customers()
setup_tracks()