import pytest
from unittest.mock import patch
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


@patch("database_connection.Database.find")
def test_find_existing_transaction_with_id(db_find_mock):
    transaction_id = 3
    expected_transaction = Transaction(primary_key=transaction_id, date="2018-12-12", category="Testing",
                                       payment_method="Credit Card", total_expense=99.99,
                                       description="This is only a test")
    db_find_mock.return_value = [transaction_id] + expected_transaction.get_list_of_values()

    found_transaction = Transaction.find(transaction_id)

    db_find_mock.assert_called_with(transaction_id)
    assert found_transaction is not None
    assert found_transaction == expected_transaction


@patch("database_connection.Database.find")
def test_returns_none_when_finding_nonexistent_transaction(db_find_mock):
    db_find_mock.return_value = []
    nonexistent_transaction_id = 999

    transaction_entry = Transaction.find(nonexistent_transaction_id)

    db_find_mock.assert_called_with(nonexistent_transaction_id)
    assert transaction_entry is None


@patch("database_connection.Database.insert")
def test_inserting_transaction_into_database(db_insert_mock, new_transaction_data):
    expected_transaction_id = 10
    db_insert_mock.return_value = expected_transaction_id

    transaction_id = Transaction.insert(new_transaction_data)

    assert transaction_id == expected_transaction_id


@patch("database_connection.Database.update")
def test_update_existing_transaction(db_update_mock, new_transaction_data):
    transaction_to_update_id = 3
    db_update_mock.return_value = transaction_to_update_id
    transaction_to_update = Transaction(primary_key=transaction_to_update_id, date="2018-12-12", category="Testing",
                                        payment_method="Credit Card", total_expense=99.99,
                                        description="This is only a test")
    expected_query_data = list(new_transaction_data.values()) + [transaction_to_update_id]

    updated_transaction_id = transaction_to_update.update(new_transaction_data)

    db_update_mock.assert_called_with(expected_query_data)
    assert updated_transaction_id == transaction_to_update_id
    assert transaction_to_update.get_data() == new_transaction_data


@patch("database_connection.Database.delete")
def test_delete_existing_transaction(db_delete_mock):
    delete_id = 3
    db_delete_mock.return_value = True

    delete_success = Transaction.delete(delete_id)

    assert delete_success is True
