import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from presenter_transaction import TransactionPresenter


@patch("presenter_transaction.Transaction.insert")
@patch("presenter_transaction.TransactionView", autospec=True)
def test_create_new_transaction(trans_view_mock, insert_mock):
    event = MagicMock()
    form_values = {
        'primary_key': None,
        'date': "1999-12-31",
        'category': "Testing",
        'payment_method': "Amazon",
        'total_expense': 99.99,
        'description': "Testing presenter transaction creation."
    }
    trans_v = MagicMock(name="transaction_view_context_var")
    trans_view_mock.return_value.__enter__.return_value = trans_v
    trans_v.get_form_values.return_value = form_values

    trans_presenter = TransactionPresenter()
    trans_presenter.create_new_transaction(event)

    insert_mock.assert_called_with(form_values)
