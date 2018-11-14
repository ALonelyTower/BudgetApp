import sqlite3
import pytest
from model_transaction import Transaction


# TODO: Refactor database objects into a context manager for conciseness


@pytest.fixture()
def new_transaction_data():
    return {
        "date": "2018/11/12",
        "category": "Gaming",
        "payment_method": "Paypal",
        "total_expense": 10.83,
        "description": "Into the Breach"
    }


@pytest.fixture()
def test_db_path():
    from pathlib import Path
    return str(Path.cwd() / "test_transaction.db")


def clear_test_database_if_exists(db_path):
    db_conn = sqlite3.connect(db_path)
    cursor = db_conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS transactions""")
    db_conn.commit()


def create_database(db_path):
    db_conn = sqlite3.connect(db_path)
    cursor = db_conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                        trans_id INTEGER PRIMARY KEY NOT NULL,
                        trans_date DATE NOT NULL,
                        trans_category CHAR(50) NOT NULL,
                        trans_payment_method CHAR(50) NOT NULL,
                        trans_total_expense DECIMAL(22, 2) NOT NULL,
                        trans_description VARCHAR(255)
                        );"""
                   )
    db_conn.commit()
    cursor.close()
    db_conn.close()


def test_find_transaction_with_id(test_db_path):
    # TODO: There's gotta be a way to clean this setup code.  Maybe look into context managers.
    clear_test_database_if_exists(test_db_path)
    create_database(test_db_path)
    inserted_data = ("2018-11-11", "Entertainment", "Chase Rewards Card", 5.42, "Subscribed to Twitch Streamer.")
    db_conn = sqlite3.connect(test_db_path)
    cursor = db_conn.cursor()
    cursor.execute("""INSERT INTO transactions (trans_date,trans_category,trans_payment_method,
                        trans_total_expense,trans_description) VALUES(?,?,?,?,?);""", inserted_data)
    db_conn.commit()
    cursor.close()
    db_conn.close()
    transaction_id = cursor.lastrowid
    Transaction.connect_to_database(test_db_path)

    transaction = Transaction.find(transaction_id)

    assert transaction.get_tuple() == inserted_data


def test_inserting_transaction_into_database(new_transaction_data, test_db_path):
    clear_test_database_if_exists(test_db_path)
    Transaction.connect_to_database(test_db_path)
    Transaction.create_transaction_table()

    transaction_id = Transaction.insert(new_transaction_data)

    transaction = Transaction.find(transaction_id)
    assert transaction.get_data() == new_transaction_data
