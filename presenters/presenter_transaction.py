from models.model_transaction import Transaction
from views.view_transaction import TransactionView


class TransactionPresenter:
    # TODO: Refactor did_user_approve_transaction to be separate:  One to show form, the other to confirm boolean
    def __init__(self, category_presenter=None):
        self._category_presenter = category_presenter
        self._subscribers = []

    def create_new_transaction(self):
        with TransactionView(title="Create New Transaction") as trans_view:
            return self._create_new_transactions(trans_view)

    def _create_new_transactions(self, trans_view):
            self._populate_category_dropdown(trans_view)
            form_accepted = trans_view.display_editable_form()
            if form_accepted:
                self._insert_newly_added_categories_from_form(trans_view)
                transaction_record = self._prepare_transaction_payload_for_insertion(trans_view)
                new_id = Transaction.insert(transaction_record)
                self._update_subscribers()
                return new_id

    def _prepare_transaction_payload_for_insertion(self, transaction_view):
        trans_dto = transaction_view.get_form_values()
        category_name = trans_dto.category.name
        trans_dto.category.id = self._category_presenter.find_id_by_name(category_name)
        return trans_dto

    def edit_transaction(self, transaction_id):
        trans_record = self._prepare_transaction_for_form(transaction_id)
        with TransactionView(title="Edit Transaction") as trans_view:
            self._populate_category_dropdown(trans_view)
            trans_view.set_form_values(trans_record)
            form_accepted = trans_view.display_editable_form()
            if form_accepted:
                self._insert_newly_added_categories_from_form(trans_view)
                updated_record = trans_view.get_form_values()
                Transaction.update(updated_record)
                self._update_subscribers()

    def _insert_newly_added_categories_from_form(self, transaction_view):
        category_list = transaction_view.get_new_categories()
        self._category_presenter.add_new_categories(category_list)

    def view_transaction(self, transaction_id):
        trans_record = self._prepare_transaction_for_form(transaction_id)
        with TransactionView(title="View Transaction") as trans_view:
            self._populate_category_dropdown(trans_view)
            trans_view.set_form_values(trans_record)
            trans_view.display_readonly_form()

    def delete_transaction(self, transaction_id):
        trans_record = self._prepare_transaction_for_form(transaction_id)
        with TransactionView(title="Delete Transaction") as trans_view:
            self._populate_category_dropdown(trans_view)
            trans_view.set_form_values(trans_record)
            if trans_view.did_user_confirm_deletion():
                Transaction.delete(transaction_id)
                self._update_subscribers()

    def _prepare_transaction_for_form(self, transaction_id):
        trans_record = Transaction.find(transaction_id)
        trans_record.category.name = self._category_presenter.find_name_by_id(trans_record.category.id)
        return trans_record

    def _populate_category_dropdown(self, transaction_view):
        categories = self._category_presenter.get_categories()
        transaction_view.set_categories(categories)

    def find_all(self):
        return Transaction.find_all()

    def register_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def _update_subscribers(self):
        for subscriber in self._subscribers:
            subscriber.update()
