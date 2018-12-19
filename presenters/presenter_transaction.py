from models.model_transaction import Transaction
from views.view_transaction import TransactionView


class TransactionPresenter:
    def __init__(self, category_presenter=None):
        self._category_presenter = category_presenter
        self._subscribers = []

    def create_new_transaction(self):
        with TransactionView(title="Create New Transaction") as trans_v:
            categories = self._category_presenter.get_categories()
            trans_v.set_categories(categories)
            if trans_v.did_user_approve_transaction():
                category_list = trans_v.get_new_categories()
                self._category_presenter.add_new_categories(category_list)
                trans_data = trans_v.get_form_values()
                trans_data['category_id'] = self._category_presenter.find_category_id_by_name(trans_data['category'])
                Transaction.insert(trans_data)
                self._update_subscriber()

    def edit_transaction(self, transaction_id):
        record = Transaction.find(transaction_id)
        with TransactionView(title="Edit Transaction") as trans_v:
            data_transfer_object = record.get_data()
            trans_v.set_form_values(data_transfer_object)
            if trans_v.did_user_approve_transaction():
                transaction_data = trans_v.get_form_values()
                Transaction.update(transaction_id, transaction_data)
                self._update_subscriber()

    def view_transaction(self, transaction_id):
        record = Transaction.find(transaction_id)
        with TransactionView(title="View Transaction") as trans_v:
            data_transfer_object = record.get_data()
            trans_v.set_form_values(data_transfer_object)
            trans_v.display_form()

    def delete_transaction(self, transaction_id):
        record = Transaction.find(transaction_id)
        with TransactionView(title="Delete Transaction") as trans_v:
            data_transfer_object = record.get_data()
            trans_v.set_form_values(data_transfer_object)
            if trans_v.did_user_confirm_deletion():
                Transaction.delete(transaction_id)
                self._update_subscriber()

    def register_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def _update_subscriber(self):
        for subscriber in self._subscribers:
            subscriber.update()
