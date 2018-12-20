import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import sentinel


from presenters.presenter_transaction import TransactionPresenter
from models.model_transaction import Transaction
from models.data_transfer_object import TransactionDTO, CategoryDTO


@pytest.fixture()
def transaction_record():
    return TransactionDTO(
        transaction_id=1,
        date="2018-01-01",
        category=CategoryDTO(1, "TestCategory"),
        payment_method="TestCreditCard",
        total_expense=1.11,
        description="TestDescription"
    )


@patch("presenters.presenter_transaction.Transaction.insert")
@patch("presenters.presenter_transaction.TransactionView", autospec=True)
def test_create_new_transaction(trans_view_mock, insert_mock, transaction_record):
    form_values = transaction_record
    trans_view_mock.return_value.__enter__.return_value = trans_view_mock
    trans_view_mock.get_form_values.return_value = form_values
    subscriber = MagicMock(name="subscriber")
    category_presenter = MagicMock(name="category_presenter")
    category_presenter.get_categories.return_value = []
    category_presenter.find_id_by_name.return_value = 1

    trans_presenter = TransactionPresenter(category_presenter)
    trans_presenter.register_subscriber(subscriber)
    trans_presenter.create_new_transaction()

    assert trans_view_mock.did_user_approve_transaction.called is True
    insert_mock.assert_called_with(form_values)
    assert subscriber.update.called


@patch("presenters.presenter_transaction.Transaction.insert")
@patch("presenters.presenter_transaction.TransactionView", autospec=True)
def test_do_not_create_new_transaction_if_user_cancels(view_mock, insert_mock):
    view_mock.return_value.__enter__.return_value = view_mock
    view_mock.did_user_approve_transaction.return_value = False
    subscriber = MagicMock(name="subscriber")
    category_presenter = MagicMock(name="category_presenter")
    category_presenter.get_categories.return_value = []

    trans_presenter = TransactionPresenter(category_presenter)
    trans_presenter.register_subscriber(subscriber)
    trans_presenter.create_new_transaction()

    assert view_mock.did_user_approve_transaction.called is True
    assert insert_mock.called is False
    assert subscriber.update.called is False


@patch("presenters.presenter_transaction.TransactionView", autospec=True)
@patch("presenters.presenter_transaction.Transaction.update")
@patch("presenters.presenter_transaction.Transaction.find")
def test_edit_transaction(find_mock, update_mock, view_mock, transaction_record):
    transaction_id = 5
    find_mock.return_value = transaction_record
    view_mock.return_value.__enter__.return_value = view_mock
    view_mock.get_form_values.return_value = transaction_record
    subscriber = MagicMock(name="subscriber")
    category_presenter = MagicMock(name="CategoryPresenter")

    trans_presenter = TransactionPresenter(category_presenter)
    trans_presenter.register_subscriber(subscriber)
    trans_presenter.edit_transaction(transaction_id)

    find_mock.assert_called_with(transaction_id)
    view_mock.set_form_values.assert_called_with(transaction_record)
    assert view_mock.did_user_approve_transaction.called is True
    assert view_mock.get_form_values.called
    update_mock.assert_called_with(transaction_record)
    assert subscriber.update.called


@patch("presenters.presenter_transaction.TransactionView", autospec=True)
@patch("presenters.presenter_transaction.Transaction.find")
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
    assert view_mock.display_form.called is True


@patch("presenters.presenter_transaction.Transaction.delete")
@patch("presenters.presenter_transaction.TransactionView", autospec=True)
@patch("presenters.presenter_transaction.Transaction.find")
def test_delete_transaction(find_mock, view_mock, delete_mock):
    transaction_id = 7
    raw_data = sentinel.raw_data
    record = MagicMock(name="transaction_mock", spec=Transaction)
    record.get_data.return_value = raw_data
    view_mock.return_value.__enter__.return_value = view_mock
    find_mock.return_value = record
    subscriber = MagicMock(name="subscriber")

    transaction_presenter = TransactionPresenter()
    transaction_presenter.register_subscriber(subscriber)
    transaction_presenter.delete_transaction(transaction_id)

    assert find_mock.called is True
    record.get_data.called is True
    assert view_mock.set_form_values.called is True
    assert view_mock.did_user_confirm_deletion.called is True
    assert delete_mock.called is True


@patch("presenters.presenter_transaction.Transaction.delete")
@patch("presenters.presenter_transaction.TransactionView", autospec=True)
@patch("presenters.presenter_transaction.Transaction.find")
def test_do_not_delete_transaction_if_user_cancels(find_mock, view_mock, delete_mock):
    transaction_id = 6
    view_mock.return_value.__enter__.return_value = view_mock
    view_mock.did_user_confirm_deletion.return_value = False
    subscriber = MagicMock(name="subscriber")

    transaction_presenter = TransactionPresenter()
    transaction_presenter.register_subscriber(subscriber)
    transaction_presenter.delete_transaction(transaction_id)

    assert delete_mock.called is False
    assert subscriber.update.called is False
