import wx
from view_budget import BudgetView
from presenter_transaction import TransactionPresenter
from view_transaction import TransactionView
from model_transaction import Transaction


class BudgetPresenter:
    def __init__(self, budget_view, trans_presenter):
        self._budget_view = budget_view
        transaction_list = Transaction.find_all()
        self._budget_view.set_transaction_list(transaction_list)
        self._trans_presenter = trans_presenter

        self._budget_view.bind_add_transaction_action(self._trans_presenter.create_new_transaction)
        self._budget_view.bind_view_transaction_action(self.view_transaction_item)
        self._budget_view.Show()

    def view_transaction_item(self, event):
        transaction_id = self._budget_view.get_selected_transaction_id()
        self._trans_presenter.view_transaction(transaction_id=transaction_id)


if __name__ == '__main__':
    app = wx.App()
    budget_v = BudgetView()
    trans_p = TransactionPresenter(TransactionView())
    budget_presenter = BudgetPresenter(budget_v, trans_p)
    app.MainLoop()
# Create New Transaction Button
# Create Edit Transaction Button
# Create ListView Transaction Button
# Create Delete Transaction Button
