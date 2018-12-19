from views.view_budget import BudgetView
from presenters.presenter_transaction import TransactionPresenter
from presenters.presenter_category import CategoryPresenter
from models.model_transaction import Transaction


class BudgetPresenter:
    def __init__(self, budget_view, transaction_presenter):
        self._budget_view = budget_view
        self._refresh_transaction_list()

        self._trans_presenter = transaction_presenter
        self._trans_presenter.register_subscriber(self)

        self._budget_view.bind_add_transaction_action(self.create_new_transaction)
        self._budget_view.bind_view_transaction_action(self.view_selected_transaction_item)
        self._budget_view.bind_edit_transaction_action(self.edit_selected_transaction_item)
        self._budget_view.bind_delete_transaction_action(self.delete_selected_transaction_item)

    def create_new_transaction(self):
        self._trans_presenter.create_new_transaction()

    def view_selected_transaction_item(self):
        transaction_id = self._budget_view.get_selected_transaction_id()
        self._trans_presenter.view_transaction(transaction_id=transaction_id)

    def edit_selected_transaction_item(self):
        transaction_id = self._budget_view.get_selected_transaction_id()
        self._trans_presenter.edit_transaction(transaction_id=transaction_id)

    def delete_selected_transaction_item(self):
        transaction_id = self._budget_view.get_selected_transaction_id()
        self._trans_presenter.delete_transaction(transaction_id=transaction_id)

    def update(self):
        self._refresh_transaction_list()

    def _refresh_transaction_list(self):
        transaction_list = Transaction.find_all()
        self._budget_view.set_transaction_list_ctrl(transaction_list)


if __name__ == '__main__':
    import wx
    app = wx.App(False)
    budget_v = BudgetView()
    categ_p = CategoryPresenter()
    trans_p = TransactionPresenter(categ_p)
    budget_presenter = BudgetPresenter(budget_v, trans_p)
    budget_v.start()
    app.MainLoop()
