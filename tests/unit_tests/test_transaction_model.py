from database_connection import DatabaseConnection
import pytest
from model_transaction import Transaction


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


@pytest.fixture()
def insert_data_list():
    return [
        ("2018-01-11", "Grocery", "Cash", 43.11, "Ran out of whole milk, and beef stew ingredients."),
        ("2018-02-23", "Utility", "Chase Visa", 1000.32, "Charter Xfinity Time Warner Cable Internet."),
        ("2018-01-11", "Maintenance", "Cash", 200.00, "Leaky ceiling repairs."),
        ("2018-01-11", "Entertainment", "US Bank Visa", 12.41, "Movie Ticket: Infinity War"),
        ("2018-01-11", "Education", "Cash", 2341.11, "College Tuition Payment"),
        ("2018-01-11", "Dine-out", "American Bank Mastercard", 41.13, "Jiro's Sushi"),
        ("2018-01-11", "Grocery", "ApplePay", 21.91, "Ingredients for Beef Curry"),
    ]


def clear_test_database_transaction_table_if_exists(db_path):
    with DatabaseConnection(db_path) as cursor:
        cursor.execute("""DROP TABLE IF EXISTS transactions""")


def create_database_transaction_table(db_path):
    with DatabaseConnection(db_path) as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                            trans_id INTEGER PRIMARY KEY NOT NULL,
                            trans_date DATE NOT NULL,
                            trans_category CHAR(50) NOT NULL,
                            trans_payment_method CHAR(50) NOT NULL,
                            trans_total_expense DECIMAL(22, 2) NOT NULL,
                            trans_description VARCHAR(255)
                            );"""
                       )


def populate_database_transaction_table_with_entries(insert_data_list, db_path):
    with DatabaseConnection(db_path) as cursor:
        for insert_sql in insert_data_list:
            cursor.execute("""INSERT INTO transactions (trans_date,trans_category,trans_payment_method,
                                trans_total_expense,trans_description) VALUES(?,?,?,?,?);""", insert_sql)


def test_find_existing_transaction_with_id(test_db_path, insert_data_list):
    clear_test_database_transaction_table_if_exists(test_db_path)
    create_database_transaction_table(test_db_path)
    populate_database_transaction_table_with_entries(insert_data_list, test_db_path)
    Transaction.set_database_path(test_db_path)
    transaction_id = 3

    found_transaction = Transaction.find(transaction_id)

    assert found_transaction.get_tuple() == insert_data_list[transaction_id - 1]


def test_returns_none_when_finding_nonexistent_transaction(test_db_path):
    clear_test_database_transaction_table_if_exists(test_db_path)
    create_database_transaction_table(test_db_path)
    Transaction.set_database_path(test_db_path)
    nonexistent_transaction_id = 999

    transaction_entry = Transaction.find(nonexistent_transaction_id)

    assert transaction_entry is None


def test_inserting_transaction_into_database(new_transaction_data, test_db_path):
    clear_test_database_transaction_table_if_exists(test_db_path)
    create_database_transaction_table(test_db_path)
    Transaction.set_database_path(test_db_path)

    transaction_id = Transaction.insert(new_transaction_data)

    transaction = Transaction.find(transaction_id)
    assert transaction.get_data() == new_transaction_data


def test_update_existing_transaction(insert_data_list, new_transaction_data, test_db_path):
    clear_test_database_transaction_table_if_exists(test_db_path)
    create_database_transaction_table(test_db_path)
    populate_database_transaction_table_with_entries(insert_data_list, test_db_path)
    Transaction.set_database_path(test_db_path)
    transaction_to_update_id = 3

    transaction_to_update = Transaction.find(transaction_to_update_id)
    transaction_to_update.update(new_transaction_data)
    updated_transaction = Transaction.find(transaction_to_update_id)

    assert updated_transaction.get_data() == new_transaction_data
    assert transaction_to_update == updated_transaction


def test_delete_existing_transaction(insert_data_list, test_db_path):
    clear_test_database_transaction_table_if_exists(test_db_path)
    create_database_transaction_table(test_db_path)
    populate_database_transaction_table_with_entries(insert_data_list, test_db_path)
    Transaction.set_database_path(test_db_path)
    delete_id = 3

    delete_success = Transaction.delete(delete_id)
    search_result = Transaction.find(delete_id)

    assert delete_success is True
    assert search_result is None
