import pytest
from unittest.mock import patch
from models.model_transaction import Transaction


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
def generate_transaction():
    num_of_transactions = 5
    return (Transaction(primary_key=count, date=f"{count}-{count}-{count}", category=f"{count} category",
            payment_method=f"{count} payment method", total_expense=float(count),
            description=f"{count} description") for count in range(num_of_transactions))


@patch("models.model_transaction.Database.find")
def test_find_existing_transaction_with_id(find_mock):
    table_name = 'transactions'
    key_column_name = 'trans_id'
    transaction_id = 3
    expected_transaction = Transaction(primary_key=transaction_id, date="2018-12-12", category="Testing",
                                       payment_method="Credit Card", total_expense=99.99,
                                       description="This is only a test")
    row = [transaction_id] + expected_transaction.get_list_of_values()
    find_mock.return_value = row

    found_transaction = Transaction.find(transaction_id)

    find_mock.assert_called_with(table_name, key_column_name, transaction_id)
    assert found_transaction is not None
    assert found_transaction == expected_transaction


@patch("models.model_transaction.Database.find")
def test_returns_none_when_finding_nonexistent_transaction(db_find_mock):
    db_find_mock.return_value = []
    nonexistent_transaction_id = 999
    table_name = "transactions"
    key_column_name = "trans_id"

    transaction_entry = Transaction.find(nonexistent_transaction_id)

    db_find_mock.assert_called_with(table_name, key_column_name, nonexistent_transaction_id)
    assert transaction_entry is None


@patch("models.model_transaction.Database.insert")
def test_inserting_transaction_into_database(db_insert_mock, new_transaction_data):
    expected_transaction_id = 10
    db_insert_mock.return_value = expected_transaction_id

    transaction_id = Transaction.insert(new_transaction_data)

    assert transaction_id == expected_transaction_id


@patch("models.model_transaction.Database.update")
def test_update_existing_transaction(db_update_mock, new_transaction_data):
    table_name = "transactions"
    column_names = ["trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description"]
    primary_key_column_name = "trans_id"
    update_id = 3
    db_update_mock.return_value = update_id
    expected_query_data = tuple(new_transaction_data.values()) + (update_id,)

    updated_transaction_id = Transaction.update(update_id, new_transaction_data)

    db_update_mock.assert_called_with(table_name, column_names, expected_query_data, primary_key_column_name)
    assert updated_transaction_id == update_id


@patch("models.model_transaction.Database.delete")
def test_delete_existing_transaction(db_delete_mock):
    delete_id = 3
    db_delete_mock.return_value = True

    delete_success = Transaction.delete(delete_id)

    assert delete_success is True


@patch("models.model_transaction.Database.find_all_transactions")
def test_find_all_transactions(db_find_all_mock, generate_transaction):
    list_of_transaction = list(generate_transaction)
    db_find_all_mock.return_value = list_of_transaction

    row_list = Transaction.find_all()

    assert list_of_transaction == row_list

