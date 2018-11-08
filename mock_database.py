class DatabaseMock:
    def __init__(self):
        self._current_record_key = 0
        self._record_storage = {}

    def insert(self, new_record_data):
        self._increment_record_key()
        self._record_storage[self._current_record_key] = new_record_data
        return self._current_record_key

    def select(self, record_id):
        return self._record_storage[record_id]

    def update(self, record_id, updated_record_data):
        self._record_storage[record_id].update(updated_record_data)
        return True

    def delete(self, record_id):
        self._record_storage[record_id] = None
        return True

    def _increment_record_key(self):
        self._current_record_key += 1
