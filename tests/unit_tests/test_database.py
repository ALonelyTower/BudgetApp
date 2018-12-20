import pytest
from unittest.mock import patch
from unittest.mock import PropertyMock


from settings import DB_PATH_TEST
from database.reset_database import reset_database
from database.populate_database import populate_database
from database.database_connection import Database
#TODO: Refactor tests to be less verbose


@pytest.fixture()
def column_names():
    return "trans_id", "trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description"


@pytest.fixture()
def update_column_names():
    return "trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description"


def test_find_query_construction(column_names):
    table_name = "transactions"
    key_column_name = "trans_id"

    expected_query = "SELECT trans_id, trans_date, category_fk, trans_payment_method, trans_total_expense, " \
                     "trans_description FROM transactions WHERE trans_id = ?"

    actual_query = Database.create_find_query(table_name, column_names, key_column_name)

    assert actual_query == expected_query


def test_insert_query_construction(column_names):
    table_name = "transactions"

    expected_query = "INSERT INTO transactions (trans_id, trans_date, category_fk, trans_payment_method, " \
                     "trans_total_expense, trans_description) VALUES (?, ?, ?, ?, ?, ?)"

    actual_query = Database.create_insert_query(table_name, column_names)

    assert actual_query == expected_query


def test_update_query_construction(update_column_names):
    table_name = "transactions"
    column_id_name = "trans_id"

    expected_query = "UPDATE transactions SET trans_date = ?, category_fk = ?, trans_payment_method = ?, " \
                     "trans_total_expense = ?, trans_description = ? WHERE trans_id = ?"

    actual_query = Database.create_update_query(table_name, update_column_names, column_id_name)

    assert actual_query == expected_query


def test_delete_query_construction():
    table_name = "transactions"
    column_id_name = "trans_id"

    expected_query = "DELETE FROM transactions WHERE trans_id = ?"

    actual_query = Database.create_delete_query(table_name, column_id_name)

    assert actual_query == expected_query


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_find(mock_db_path, column_names):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    table_name = "transactions"
    key_column_name = "trans_id"
    table_id = 4
    expected_result = (4, "2018-01-11", 5, "US Bank Visa", 12.41, "Movie Ticket: Infinity War")

    actual_result = Database.find(table_name, column_names, key_column_name, table_id)

    assert actual_result == expected_result


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_insert(mock_db_path, column_names, update_column_names):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    expected_id = 1
    expected_result = (1, '2000-01-01', 1, 'Cash', 1.11, 'This is a test.')
    table_name = "transactions"
    key_column_name = "trans_id"
    table_values = ("2000-01-01", "1", "Cash", 1.11, "This is a test.")

    trans_id = Database.insert(table_name, update_column_names, table_values)
    actual_result = Database.find(table_name, column_names, key_column_name, trans_id)

    assert trans_id == expected_id
    assert actual_result == expected_result


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_update_transaction_full(mock_db_path, column_names, update_column_names):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    table_name = "transactions"
    key_column_name = "trans_id"
    record_id_to_update = 4
    updated_values = ("1999-12-12", 4, "Credit Card", 2.22, "This is an updated test.", record_id_to_update)
    expected_record = (record_id_to_update, "1999-12-12", 4, "Credit Card", 2.22, "This is an updated test.")
    primary_key_column_name = "trans_id"

    update_success = Database.update(table_name, update_column_names, updated_values, primary_key_column_name)

    updated_record = Database.find(table_name, column_names, key_column_name, record_id_to_update)

    assert update_success
    assert updated_record == expected_record


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_delete_transaction(mock_db_path, column_names):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    table_name = "transactions"
    key_column_name = "trans_id"
    record_delete_id = 3

    delete_success = Database.delete(record_delete_id, table_name, key_column_name)

    delete_search_result = Database.find(table_name, column_names, key_column_name, record_delete_id)

    assert delete_success
    assert delete_search_result is None

