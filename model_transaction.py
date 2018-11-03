

class TransactionModel:
    def __init__(self, database):
        self._database = database

    def create(self, transaction_data):
        self._database.create(transaction_data)

    def read(self, transaction_id):
        return self._database.read(transaction_id)

    def update(self, transaction_id, transaction_data):
        self._database.update(transaction_id, transaction_data)

    def delete(self, transaction_id):
        self._database.delete(transaction_id)
