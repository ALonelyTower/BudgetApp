from data_storage.database import Database
from models.data_transfer_object import CategoryDTO


class Category:
    _table_name = "categories"
    _column_id_name = "cate_id"
    _column_label_name = "cate_name"
    _column_names = [_column_id_name, _column_label_name]

    @classmethod
    def insert(cls, name):
        # TODO: Think of more readable way to either convert values to tuple for insertion method
        return Database.insert(cls._table_name, (cls._column_label_name,), (name,))

    @classmethod
    def find_by_name(cls, name):
        return Database.find(cls._table_name, cls._column_names, cls._column_label_name, name)

    @classmethod
    def find_by_id(cls, category_id):
        return Database.find(cls._table_name, cls._column_id_name, category_id)

    @classmethod
    def find_all(cls):
        query_results = Database.find_all_categories()
        return [CategoryDTO(*query_result) for query_result in query_results]
