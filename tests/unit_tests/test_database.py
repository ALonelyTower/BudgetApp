import pytest
from unittest.mock import patch
from unittest.mock import PropertyMock


from settings import DB_PATH_TEST
from database.reset_database import reset_database
from database.populate_database import populate_database
from database.database_connection import Database
# TODO: Refactor tests to be less verbose


@pytest.fixture()
def transaction_columns_select():
    return "trans_id", "trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description"


@pytest.fixture()
def transaction_columns_insert():
    return "trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description"


@pytest.fixture()
def transaction_columns_update():
    return "trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description"


@pytest.fixture()
def category_columns_select():
    return "cate_id", "cate_name"


@pytest.fixture()
def category_columns_insert():
    return "cate_name",


def test_find_transaction_query_construction(transaction_columns_select):
    table_name = "transactions"
    key_column_name = "trans_id"

    expected_query = "SELECT trans_id, trans_date, category_fk, trans_payment_method, trans_total_expense, " \
                     "trans_description FROM transactions WHERE trans_id = ?"

    actual_query = Database.create_find_query(table_name, transaction_columns_select, key_column_name)

    assert actual_query == expected_query


def test_find_category_query_construction(category_columns_select):
    table_name = "categories"
    key_column_name = "cate_id"

    expected_query = "SELECT cate_id, cate_name FROM categories WHERE cate_id = ?"

    actual_query = Database.create_find_query(table_name, category_columns_select, key_column_name)

    assert actual_query == expected_query


def test_insert_transaction_query_construction(transaction_columns_insert):
    table_name = "transactions"

    expected_query = "INSERT INTO transactions (trans_date, category_fk, trans_payment_method, " \
                     "trans_total_expense, trans_description) VALUES (?, ?, ?, ?, ?)"

    actual_query = Database.create_insert_query(table_name, transaction_columns_insert)

    assert actual_query == expected_query


def test_insert_category_query_construction(category_columns_insert):
    table_name = "categories"

    expected_query = "INSERT INTO categories (cate_name) VALUES (?)"

    actual_query = Database.create_insert_query(table_name, category_columns_insert)

    assert actual_query == expected_query


def test_update_transaction_query_construction(transaction_columns_update):
    table_name = "transactions"
    column_id_name = "trans_id"

    expected_query = "UPDATE transactions SET trans_date = ?, category_fk = ?, trans_payment_method = ?, " \
                     "trans_total_expense = ?, trans_description = ? WHERE trans_id = ?"

    actual_query = Database.create_update_query(table_name, transaction_columns_update, column_id_name)

    assert actual_query == expected_query


def test_update_categories_query_construction(category_columns_insert):
    table_name = "categories"
    column_id_name = "cate_id"

    expected_query = "UPDATE categories SET cate_name = ? WHERE cate_id = ?"

    actual_query = Database.create_update_query(table_name, category_columns_insert, column_id_name)

    assert actual_query == expected_query


def test_delete_transaction_query_construction():
    table_name = "transactions"
    column_id_name = "trans_id"

    expected_query = "DELETE FROM transactions WHERE trans_id = ?"

    actual_query = Database.create_delete_query(table_name, column_id_name)

    assert actual_query == expected_query


def test_delete_categories_query_construction():
    table_name = "categories"
    column_id_name = "cate_id"

    expected_query = "DELETE FROM categories WHERE cate_id = ?"

    actual_query = Database.create_delete_query(table_name, column_id_name)

    assert actual_query == expected_query


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_find_for_transaction(mock_db_path, transaction_columns_select):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    table_name = "transactions"
    key_column_name = "trans_id"
    table_id = 4
    expected_result = (4, "2018-01-11", 5, "US Bank Visa", 12.41, "Movie Ticket: Infinity War")

    actual_result = Database.find(table_name, transaction_columns_select, key_column_name, table_id)

    assert actual_result == expected_result


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_find_for_categories(mock_db_path, category_columns_select):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    table_name = "categories"
    key_column_name = "cate_id"
    category_id = 3
    expected_result = (3, "Insurance")

    actual_result = Database.find(table_name, category_columns_select, key_column_name, category_id)

    assert actual_result == expected_result


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_insert_for_transaction(mock_db_path, transaction_columns_insert, transaction_columns_select):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    expected_id = 1
    expected_result = (1, '2000-01-01', 1, 'Cash', 1.11, 'This is a test.')
    table_name = "transactions"
    key_column_name = "trans_id"
    table_values = ("2000-01-01", "1", "Cash", 1.11, "This is a test.")

    trans_id = Database.insert(table_name, transaction_columns_insert, table_values)
    actual_result = Database.find(table_name, transaction_columns_select, key_column_name, trans_id)

    assert trans_id == expected_id
    assert actual_result == expected_result


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_insert_for_categories(mock_db_path, category_columns_select, category_columns_insert):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    expected_id = 13
    expected_result = (13, "TestCategory")
    table_name = "categories"
    key_column_name = "cate_id"
    table_values = ("TestCategory",)

    cate_id = Database.insert(table_name, category_columns_insert, table_values)
    actual_result = Database.find(table_name, category_columns_select, key_column_name, cate_id)

    assert cate_id == expected_id
    assert actual_result == expected_result


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_update_transaction_full(mock_db_path, transaction_columns_select, transaction_columns_update):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    table_name = "transactions"
    key_column_name = "trans_id"
    record_id_to_update = 4
    updated_values = ("1999-12-12", 4, "Credit Card", 2.22, "This is an updated test.", record_id_to_update)
    expected_record = (record_id_to_update, "1999-12-12", 4, "Credit Card", 2.22, "This is an updated test.")
    primary_key_column_name = "trans_id"

    update_success = Database.update(table_name, transaction_columns_update, updated_values, primary_key_column_name)

    updated_record = Database.find(table_name, transaction_columns_select, key_column_name, record_id_to_update)

    assert update_success
    assert updated_record == expected_record


@patch("database.database_connection.Database._database_path", new_callable=PropertyMock)
def test_database_delete_transaction(mock_db_path, transaction_columns_insert):
    mock_db_path.return_value = DB_PATH_TEST
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)
    table_name = "transactions"
    key_column_name = "trans_id"
    record_delete_id = 3

    delete_success = Database.delete(record_delete_id, table_name, key_column_name)

    delete_search_result = Database.find(table_name, transaction_columns_insert, key_column_name, record_delete_id)

    assert delete_success
    assert delete_search_result is None

