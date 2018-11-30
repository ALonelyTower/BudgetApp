import pytest


from database_connection import DatabaseConnection
from model_transaction import Transaction
import sql_scripts
import settings


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
    return settings.DB_PATH


@pytest.fixture()
def insert_data_list():
    import json
    from pathlib import Path
    cwd = Path.cwd()
    parent = cwd.parent

    with open(parent / "fixtures\\transaction_data.json") as json_fp:
        trans_dict = json.load(json_fp)
    return list(trans_dict.values())


def populate_database_transaction_table_with_entries(db_path, insert_data_list):
    with DatabaseConnection(db_path) as cursor:
        for insert_sql in insert_data_list:
            cursor.execute(sql_scripts.insert_transaction_query, insert_sql)


def load_test_database(db_path):
    with DatabaseConnection(db_path) as cursor:
        cursor.execute(sql_scripts.drop_transaction_table_query)

    with DatabaseConnection(db_path) as cursor:
        cursor.execute(sql_scripts.create_transaction_table_query)


def test_find_existing_transaction_with_id(test_db_path, insert_data_list):
    load_test_database(test_db_path)
    populate_database_transaction_table_with_entries(test_db_path, insert_data_list)
    transaction_id = 3

    found_transaction = Transaction.find(transaction_id)

    assert found_transaction.get_list() == insert_data_list[transaction_id - 1]


def test_returns_none_when_finding_nonexistent_transaction(test_db_path):
    load_test_database(test_db_path)
    nonexistent_transaction_id = 999

    transaction_entry = Transaction.find(nonexistent_transaction_id)

    assert transaction_entry is None


def test_inserting_transaction_into_database(new_transaction_data, test_db_path):
    load_test_database(test_db_path)

    transaction_id = Transaction.insert(new_transaction_data)

    transaction = Transaction.find(transaction_id)
    assert transaction.get_data() == new_transaction_data


def test_update_existing_transaction(insert_data_list, new_transaction_data, test_db_path):
    load_test_database(test_db_path)
    populate_database_transaction_table_with_entries(test_db_path, insert_data_list)
    transaction_to_update_id = 3

    transaction_to_update = Transaction.find(transaction_to_update_id)
    transaction_to_update.update(new_transaction_data)
    updated_transaction = Transaction.find(transaction_to_update_id)

    assert updated_transaction.get_data() == new_transaction_data
    assert transaction_to_update == updated_transaction


def test_delete_existing_transaction(insert_data_list, test_db_path):
    load_test_database(test_db_path)
    populate_database_transaction_table_with_entries(test_db_path, insert_data_list)
    delete_id = 3

    delete_success = Transaction.delete(delete_id)
    search_result = Transaction.find(delete_id)

    assert delete_success is True
    assert search_result is None
