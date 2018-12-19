from database.database_connection import Database
from models.model_category import Category


class Transaction:
    # TODO: Check if cursor.lastrowid is not influenced by others also interacting with the database
    _table_name = "transactions"
    _key_column_name = "trans_id"
    _column_names = ["trans_date", "category_fk", "trans_payment_method", "trans_total_expense", "trans_description"]

    def __init__(self, primary_key, date, category, payment_method, total_expense, description):
        self.primary_key = primary_key
        self.date = date
        self.category = category
        self.payment_method = payment_method
        self.total_expense = total_expense
        self.description = description

    @classmethod
    def insert(cls, insert_data):
        inserted_data = (insert_data['date'], insert_data['category_id'], insert_data['payment_method'],
                         insert_data['total_expense'], insert_data['description'])

        new_transaction_id = Database.insert(cls._table_name, cls._column_names, inserted_data)

        return new_transaction_id

    @classmethod
    def update(cls, transaction_id, update_data):
        # TODO:  Figure out a better way to update instance variables, and output sql statement for update
        update_data = (update_data['date'], update_data['category'], update_data['category_id'],
                       update_data['payment_method'], update_data['total_expense'], update_data['description'],
                       transaction_id)

        updated_transaction_id = Database.update(cls._table_name, cls._column_names, update_data, cls._key_column_name)

        return updated_transaction_id

    @classmethod
    def delete(cls, delete_id):
        # TODO: Find out what happens when it tries to delete something that doesn't exist
        return Database.delete(delete_id, cls._table_name, cls._key_column_name)

    @classmethod
    def find(cls, transaction_id):
        transaction_record = None

        if transaction_id is None:
            raise TypeError(f"Invalid Transaction Id Given: {transaction_id}")

        row = Database.find(cls._table_name, cls._key_column_name, transaction_id)
        if row:
            transaction_record = Transaction(primary_key=row[0], date=row[1], category=row[2],
                                             payment_method=row[3], total_expense=row[4], description=row[5])

        return transaction_record

    @classmethod
    def find_all(cls):
        # TODO: Convert Rows into Transaction objects
        return Database.find_all_transactions()

    def get_data(self):
        return {
            "date": self.date,
            "category": self.category,
            "payment_method": self.payment_method,
            "total_expense": self.total_expense,
            "description": self.description,
        }

    def get_list_of_values(self):
        return [
            self.date,
            self.category,
            self.payment_method,
            self.total_expense,
            self.description,
        ]

    def __eq__(self, other):
        return self.get_data() == other.get_data()

    def __repr__(self):
        return f"Transaction({self.primary_key}, '{self.date}', '{self.category}', {self.payment_method}, " \
                f"'{self.description}')"


