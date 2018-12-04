from model_transaction import Transaction


class TransactionPresenter:
    def __init__(self, transaction_view):
        self._transaction_view = transaction_view
        self._subscribers = []

    def create_new_transaction(self, event):
        # Look into Interactor to remove requirement for event parameter
        if self._transaction_view.is_user_adding_or_changing_transaction():
            transaction_data = self._transaction_view.get_form_values()
            Transaction.insert(transaction_data)
            self._update_subscriber()

    def edit_transaction(self, event, transaction_id):
        record = Transaction.find(transaction_id)
        self._transaction_view.set_form_values(record.get_data())
        if self._transaction_view.is_user_adding_or_changing_transaction():
            transaction_data = self._transaction_view.get_form_values()
            record.update(transaction_data)

    def view_transaction(self, transaction_id):
        record = Transaction.find(transaction_id)
        self._transaction_view.set_form_values(record.get_data())
        self._transaction_view.display_view_form()

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