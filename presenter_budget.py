from view_budget import BudgetView
from presenter_transaction import TransactionPresenter
from view_transaction import TransactionView
from model_transaction import Transaction


class BudgetPresenter:
    def __init__(self, budget_view, trans_presenter):
        self._budget_view = budget_view
        self._refresh_transaction_list()

        self._trans_presenter = trans_presenter
        self._trans_presenter.register_subscriber(self)

        self._budget_view.bind_add_transaction_action(self._trans_presenter.create_new_transaction)
        self._budget_view.bind_view_transaction_action(self.view_transaction_item)

    def _refresh_transaction_list(self):
        transaction_list = Transaction.find_all()
        self._budget_view.set_transaction_list_ctrl(transaction_list)

    def view_transaction_item(self, event):
        transaction_id = self._budget_view.get_selected_transaction_id()
        self._trans_presenter.view_transaction(transaction_id=transaction_id)

    def update(self):
        self._refresh_transaction_list()


if __name__ == '__main__':
    import wx
    app = wx.App(False)
    budget_v = BudgetView()
    trans_p = TransactionPresenter()
    budget_presenter = BudgetPresenter(budget_v, trans_p)
    budget_v.start()
    app.MainLoop()

# Create New Transaction Button
# Create Edit Transaction Button
# Create ListView Transaction Button
# Create Delete Transaction Button
