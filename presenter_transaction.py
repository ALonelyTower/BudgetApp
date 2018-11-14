from model_transaction import Transaction


class TransactionPresenter:
    def __init__(self, transaction_view):
        self._transaction_view = transaction_view

    def create_new_transaction(self):
        if self._transaction_view.is_user_adding_or_changing_transaction():
            transaction_data = self._transaction_view.get_form_values()
            Transaction.insert(transaction_data)
