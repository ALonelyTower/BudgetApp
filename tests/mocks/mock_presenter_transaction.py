from presenters.presenter_transaction import TransactionPresenter


class MockTransactionPresenter(TransactionPresenter):
    def __init__(self, category_presenter):
        super().__init__(category_presenter)

    def create_new_transaction(self, trans_view):
        return super()._create_new_transactions(trans_view)

    def populate_category_dropdown(self, transaction_view):
        super()._populate_category_dropdown(transaction_view)

    def _populate_category_dropdown(self, transaction_view):
        pass
