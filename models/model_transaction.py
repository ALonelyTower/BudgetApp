from data_storage.database import Database
from models.data_transfer_object import TransactionDTO


class Transaction:
    # TODO: Check if cursor.lastrowid is not influenced by others also interacting with the database
    _table_name = "transactions"
    _key_column_name = "trans_id"
    _column_names = ("trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description")

    @classmethod
    def insert(cls, transaction_record):
        insert_data = transaction_record.prepare_values_for_insert()
        new_transaction_id = Database.insert(cls._table_name, cls._column_names, insert_data)

        return new_transaction_id

    @classmethod
    def update(cls, transaction_record):
        update_data = transaction_record.prepare_values_for_update()
        updated_transaction_id = Database.update(cls._table_name, cls._column_names, update_data, cls._key_column_name)

        return updated_transaction_id

    @classmethod
    def delete(cls, delete_id):
        # TODO: Find out what happens when it tries to delete something that doesn't exist
        return Database.delete(delete_id, cls._table_name, cls._key_column_name)

    @classmethod
    def find(cls, transaction_id: int) -> TransactionDTO:

        if transaction_id is None:
            raise TypeError(f"Invalid Transaction Id Given: {transaction_id}")

        select_column_names = (cls._key_column_name,) + cls._column_names
        query_result = Database.find(cls._table_name, select_column_names, cls._key_column_name, transaction_id)

        try:
            transaction_record = TransactionDTO(*query_result)
        except TypeError:
            transaction_record = None

        return transaction_record

    @classmethod
    def find_all(cls):
        rows = Database.find_all_transactions_with_categories()

        if not rows:
            return []
        else:
            return [TransactionDTO(*row) for row in rows]


