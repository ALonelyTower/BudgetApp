import mock_database


class TransactionModel:
    # TODO: Move test objects into own unit test file.
    def __init__(self, database):
        self._database = database

    def create(self, transaction_data):
        return self._database.insert(transaction_data)

    def read(self, transaction_id):
        return self._database.select(transaction_id)

    def update(self, transaction_id, transaction_data):
        return self._database.update(transaction_id, transaction_data)

    def delete(self, transaction_id):
        return self._database.delete(transaction_id)


if __name__ == '__main__':
    new_record = {
        'date': '2018/11/08',
        'category': 'grocery',
        'payment_method': 'Paypal',
        'total_expense': '$9.99',
        'description': 'Milk and Eggs',
    }

    mock_database = mock_database.DatabaseMock()
    transaction_model = TransactionModel(mock_database)

    record_key = transaction_model.create(new_record)
    print(f"New Record Key: {record_key}")
    print(transaction_model.read(record_key))
    update_record = {
        'category': 'movie rental',
    }
    transaction_model.update(record_key, update_record)
    print(transaction_model.read(record_key))

    transaction_model.delete(record_key)
    print(f"Expected Result should be None: {transaction_model.read(1)}")



