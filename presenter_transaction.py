import wx
import view_transaction


class TransactionPresenter:
    # TODO: Create function to have presenter indirectly call wx.Dialog.ShowModal to remove wx dependency
    def __init__(self, transaction_view, transaction_model):
        self._transaction_view = transaction_view
        self._transaction_model = transaction_model

    def create_new_transaction(self):
        if self._transaction_view.ShowModal() == wx.ID_OK:
            transaction_data = self._transaction_view.get_form_values()
            self._transaction_model.create(transaction_data)


if __name__ == '__main__':
    app = wx.App()
    view = view_transaction.TransactionView()
    presenter = TransactionPresenter(view)
    presenter.create_new_transaction()
    app.MainLoop()