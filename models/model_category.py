from database.database_connection import Database


class Category:
    _category_session_list = []
    _category_table_name = "categories"
    _category_column_id_name = "cate_id"
    _category_column_label_name = "cate_name"
    _column_names = [_category_column_id_name, _category_column_label_name]

    def __init__(self):
        pass

    @classmethod
    def insert(cls, name):
        return Database.insert(cls._category_table_name, cls._category_column_label_name, name)

    @classmethod
    def find_by_name(cls, name):
        return Database.find(cls._category_table_name, cls._category_column_label_name, name)

    @classmethod
    def find_all(cls):
        return Database.find_all_categories()
