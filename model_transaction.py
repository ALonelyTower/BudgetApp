from database_connection import DatabaseConnection
import settings
import sql_scripts
from database_connection import Database


class Transaction:
    # TODO: Check if cursor.lastrowid is not influenced by others also interacting with the database
    # TODO: Eventually encapsulate SQL queries in its own class (maybe SqliteDatabaseConnection)
    # TODO: Shift from classmethods to staticmethods.  Doesn't seem needed to pass classes.
    _database_path = settings.DB_PATH

    def __init__(self, primary_key, date, category, payment_method, total_expense, description):
        self._primary_key = primary_key
        self._date = date
        self._category = category
        self._payment_method = payment_method
        self._total_expense = total_expense
        self._description = description

    @classmethod
    def insert(cls, insert_data):
        inserted_data = (insert_data['date'], insert_data['category'], insert_data['payment_method'],
                         insert_data['total_expense'], insert_data['description'])

        new_transaction_id = Database.insert(inserted_data)

        return new_transaction_id

    def update(self, update_data):
        # TODO:  Figure out a better way to update instance variables, and output sql statement for update
                # Issue might resolve itself when we encapsulate the SQL into its own class.
        self._date = update_data['date']
        self._category = update_data['category']
        self._payment_method = update_data['payment_method']
        self._total_expense = update_data['total_expense']
        self._description = update_data['description']

        update_sql_data = self.get_list_of_values() + [self._primary_key, ]

        updated_transaction_id = Database.update(update_sql_data)

        return updated_transaction_id

    @classmethod
    def delete(cls, delete_id):
        # TODO: Look into scope issues inside and outside of context managers.
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
        return Database.find_all()

    def get_data(self):
        return {
            "date": self._date,
            "category": self._category,
            "payment_method": self._payment_method,
            "total_expense": self._total_expense,
            "description": self._description,
        }

    def get_list_of_values(self):
        return [
            self._date,
            self._category,
            self._payment_method,
            self._total_expense,
            self._description,
        ]

    def _ordered_member_list(self):
        return self._date, self._category, self._payment_method, self._total_expense, self._description

    def __eq__(self, other):
        return self.get_data() == other.get_data()

    def __repr__(self):
        return f"Transaction({self._primary_key}, '{self._date}', '{self._category}', {self._payment_method}, " \
                f"'{self._description}')"


