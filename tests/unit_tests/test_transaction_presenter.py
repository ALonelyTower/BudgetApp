import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import sentinel


from presenter_transaction import TransactionPresenter
from model_transaction import Transaction


@patch("presenter_transaction.Transaction.insert")
@patch("presenter_transaction.TransactionView", autospec=True)
def test_create_new_transaction(trans_view_mock, insert_mock):
    form_values = sentinel.form_values
    trans_view_mock.return_value.__enter__.return_value = trans_view_mock
    trans_view_mock.get_form_values.return_value = form_values
    subscriber = MagicMock(name="subscriber")

    trans_presenter = TransactionPresenter()
    trans_presenter.register_subscriber(subscriber)
    trans_presenter.create_new_transaction()

    assert trans_view_mock.did_user_approve_transaction.called is True
    insert_mock.assert_called_with(form_values)
    assert subscriber.update.called


@patch("presenter_transaction.TransactionView", autospec=True)
@patch("presenter_transaction.Transaction.update")
@patch("presenter_transaction.Transaction.find")
def test_edit_transaction(find_mock, update_mock, view_mock):
    transaction_id = 5
    raw_data = sentinel.raw_data
    record = MagicMock(name="transaction_mock", spec=Transaction)
    record.get_data.return_value = raw_data
    find_mock.return_value = record
    view_mock.return_value.__enter__.return_value = view_mock
    view_mock.get_form_values.return_value = raw_data
    subscriber = MagicMock(name="subscriber")

    trans_presenter = TransactionPresenter()
    trans_presenter.register_subscriber(subscriber)
    trans_presenter.edit_transaction(transaction_id)

    find_mock.assert_called_with(transaction_id)
    view_mock.set_form_values.assert_called_with(raw_data)
    assert view_mock.did_user_approve_transaction.called is True
    assert view_mock.get_form_values.called
    update_mock.assert_called_with(transaction_id, raw_data)
    assert subscriber.update.called


@patch("presenter_transaction.TransactionView", autospec=True)
@patch("presenter_transaction.Transaction.find")
def test_view_transaction(find_mock, view_mock):
    transaction_id = 7
    raw_data = sentinel.raw_data
    record = MagicMock(name="transaction_mock", spec=Transaction)
    record.get_data.return_value = raw_data
    find_mock.return_value = record
    view_mock.return_value.__enter__.return_value = view_mock
    view_mock.get_form_values.return_value = raw_data

    trans_presenter = TransactionPresenter()
    trans_presenter.view_transaction(transaction_id)

    assert find_mock.called is True
    assert record.get_data.called is True
    view_mock.set_form_values.assert_called_with(raw_data)
    assert view_mock.display_view_form.called is True


