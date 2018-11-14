import sqlite3


class Transaction:
    # TODO: Refactor database / sql out of Transaction.
    _conn = None

    def __init__(self, primary_key, date, category, payment_method, total_expense, description):
        self._primary_key = primary_key
        self._date = date
        self._category = category
        self._payment_method = payment_method
        self._total_expense = total_expense
        self._description = description

    @classmethod
    def insert(cls, insert_data):
        cursor = cls._conn.cursor()
        inserted_data = (insert_data['date'], insert_data['category'], insert_data['payment_method'],
                         insert_data['total_expense'], insert_data['description'])
        cursor.execute("""INSERT INTO transactions (trans_date,trans_category,trans_payment_method,
                            trans_total_expense,trans_description) VALUES(?,?,?,?,?);""", inserted_data)
        cls._conn.commit()
        inserted_transaction_id = cursor.lastrowid
        cursor.close()
        return inserted_transaction_id

    @classmethod
    def connect_to_database(cls, database_path):
        if cls._conn is None:
            cls._conn = sqlite3.connect(database_path)

    @classmethod
    def create_transaction_table(cls):
        cursor = cls._conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                               trans_id INTEGER PRIMARY KEY NOT NULL,
                               trans_date DATE NOT NULL,
                               trans_category CHAR(50) NOT NULL,
                               trans_payment_method CHAR(50) NOT NULL,
                               trans_total_expense DECIMAL(22, 2) NOT NULL,
                               trans_description VARCHAR(255)
                               );"""
                       )
        cls._conn.commit()

    @classmethod
    def find(cls, transaction_id):
        first_row = 0
        cursor = cls._conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE trans_id = (?)", (transaction_id,))
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            row = rows[first_row]
            return Transaction(primary_key=row[0], date=row[1], category=row[2], payment_method=row[3],
                               total_expense=row[4],
                               description=row[5])
        else:
            print("Rows are empty.")
            return 0

    def get_data(self):
        return {
            "date": self._date,
            "category": self._category,
            "payment_method": self._payment_method,
            "total_expense": self._total_expense,
            "description": self._description,
        }

    def get_tuple(self):
        return (
            self._date,
            self._category,
            self._payment_method,
            self._total_expense,
            self._description,
        )

    def _ordered_member_list(self):
        return self._date, self._category, self._payment_method, self._total_expense, self._description



