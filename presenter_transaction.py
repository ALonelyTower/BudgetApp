from model_transaction import Transaction
from view_transaction import TransactionView


class TransactionPresenter:
    def __init__(self):
        self._subscribers = []

    def create_new_transaction(self, event):
        # Look into Interactor to remove requirement for event parameter
        with TransactionView() as trans_v:
            if trans_v.is_user_adding_or_changing_transaction():
                transaction_data = trans_v.get_form_values()
                Transaction.insert(transaction_data)
                self._update_subscriber()

    def edit_transaction(self, event, transaction_id):
        record = Transaction.find(transaction_id)
        with TransactionView() as trans_v:
            trans_v.set_form_values(record.get_data())
            if trans_v.is_user_adding_or_changing_transaction():
                transaction_data = trans_v.get_form_values()
                record.update(transaction_data)

    def view_transaction(self, transaction_id):
        record = Transaction.find(transaction_id)
        with TransactionView() as trans_v:
            trans_v.set_form_values(record.get_data())
            trans_v.display_view_form()

    def register_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def _update_subscriber(self):
        for subscriber in self._subscribers:
            subscriber.update()

    """
    What is my hangup:
        I want to avoid passing around primary keys, but is that really an issue?  It's something you need to do anything,
        so why not make it a public (get) variable.
        Should the view also hold onto the primary key?  Even though it's not going to be displayed to the user, or be
        interactable at all?  Does that expose my program to dangers, such as the user arbitrarily changing the primary
        key associated with that view? (Assuming that's possible)
    """