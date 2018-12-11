from database.database_connection import Database
from data_descriptors import DateDescriptor
from data_descriptors import CashDescriptor
from data_descriptors import TextDescriptor


class Transaction:
    # TODO: Check if cursor.lastrowid is not influenced by others also interacting with the database

    def __init__(self, primary_key, date, category, payment_method, total_expense, description):
        self.primary_key = primary_key
        self.date = DateDescriptor(date)
        self.category = TextDescriptor(category)
        self.payment_method = TextDescriptor(payment_method)
        self.total_expense = CashDescriptor(total_expense)
        self.description = TextDescriptor(description)

    @classmethod
    def insert(cls, insert_data):
        inserted_data = (insert_data['date'], insert_data['category'], insert_data['payment_method'],
                         insert_data['total_expense'], insert_data['description'])

        new_transaction_id = Database.insert(inserted_data)

        return new_transaction_id

    @classmethod
    def update(cls, transaction_id, update_data):
        # TODO:  Figure out a better way to update instance variables, and output sql statement for update
        update_data = (update_data['date'], update_data['category'], update_data['payment_method'],
                       update_data['total_expense'], update_data['description'], transaction_id)

        updated_transaction_id = Database.update(update_data)

        return updated_transaction_id

    @classmethod
    def delete(cls, delete_id):
        # TODO: Find out what happens when it tries to delete something that doesn't exist
        return Database.delete(delete_id)

    @classmethod
    def find(cls, transaction_id):
        transaction_record = None

        if transaction_id is None:
            raise TypeError(f"Invalid Transaction Id Given: {transaction_id}")

        row = Database.find(transaction_id)
        if row:
            transaction_record = Transaction(primary_key=row[0], date=row[1], category=row[2],
                                             payment_method=row[3], total_expense=row[4], description=row[5])

        return transaction_record

    @classmethod
    def find_all(cls):
        # TODO: Convert Rows into Transaction objects
        return Database.find_all()

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
            self.date.date,
            self.category.text,
            self.payment_method.text,
            self.total_expense.cash,
            self.description.text,
        ]

    def _ordered_member_list(self):
        return self.date, self.category, self.payment_method, self.total_expense, self.description

    def __eq__(self, other):
        return self.get_data() == other.get_data()

    def __repr__(self):
        return f"Transaction({self.primary_key}, '{self.date}', '{self.category}', {self.payment_method}, " \
                f"'{self.description}')"


