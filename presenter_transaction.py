import view_transaction
import model_transaction
import mock_database


class TransactionPresenter:
    def __init__(self, transaction_view, transaction_model):
        self._transaction_view = transaction_view
        self._transaction_model = transaction_model

    def create_new_transaction(self):
        if self._transaction_view.is_user_adding_or_changing_transaction():
            transaction_data = self._transaction_view.get_form_values()
            self._transaction_model.create(transaction_data)


if __name__ == '__main__':
    import wx
    app = wx.App()
    view = view_transaction.TransactionView()
    database = mock_database.DatabaseMock()
    model = model_transaction.TransactionModel(database)
    presenter = TransactionPresenter(view, model)
    presenter.create_new_transaction()
    print(model.read(1))
    app.MainLoop()
