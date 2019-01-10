from tests.mocks.mock_presenter_transaction import MockTransactionPresenter
from tests.mocks.mock_view_transaction import MockTransactionView
from presenters.presenter_category import CategoryPresenter
from models.data_transfer_object import TransactionDTO, CategoryDTO
from models.model_transaction import Transaction
from data_storage.database import Database
from data_storage.reset_database import reset_database
from data_storage.populate_database import populate_database
from settings import DB_PATH_TEST

import wx


def test_submit_transaction_form_into_database():
    # Database setup
    Database.set_database_path(DB_PATH_TEST)
    reset_database(DB_PATH_TEST)
    populate_database(DB_PATH_TEST)

    # Instantiate required objects
    app = wx.App()
    new_category = CategoryDTO.new("Entertainment")
    form_data = TransactionDTO.new("2000-01-01", new_category, "TestCredit", 1.11, "TestDescription")
    trans_view = MockTransactionView(title="Create New Transaction")
    category_presenter = CategoryPresenter()
    trans_presenter = MockTransactionPresenter(category_presenter)
    trans_presenter.populate_category_dropdown(trans_view)

    # Populate Form with Values from TransactionDTO
    trans_view.set_form_values(form_data)

    # After Form appears, fire off 'Ok Button' event.
    milliseconds_to_wait = 500
    wx.CallLater(milliseconds_to_wait, trans_view.EndModal, wx.ID_OK)

    # Execute Form, and insert into Database
    insert_id = trans_presenter.create_new_transaction(trans_view)
    trans_view.Destroy()
    app.MainLoop()

    # Get the record from the database and verify it matches what we expect.
    inserted_transaction = Transaction.find(insert_id)

    assert inserted_transaction == TransactionDTO(8, "2000-01-01", CategoryDTO(5, ""), "TestCredit", 1.11, "TestDescription")



