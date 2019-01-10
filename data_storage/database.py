import settings
from data_storage import sql_scripts
from data_storage.database_connection import DatabaseConnection


class Database:
    _database_path = settings.DB_PATH

    @classmethod
    def set_database_path(cls, db_path):
        # For test convenience.
        cls._database_path = db_path

    @classmethod
    def insert(cls, table_name: str, column_names: tuple, column_values: tuple) -> int:
        query_statement = Database.create_insert_query(table_name, column_names)
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(query_statement, column_values)
            return cursor.lastrowid

    @classmethod
    def _is_it_a_container(cls, value):
        try:
            return isinstance(value, (list, tuple))
        except TypeError:
            return False

    @classmethod
    def update(cls, table_name, column_names, updated_values, primary_key_column_name):
        query_statement = Database.create_update_query(table_name, column_names, primary_key_column_name)
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(query_statement, updated_values)
            return True

    @classmethod
    def delete(cls, delete_id, table_name, key_column_name):
        query_statement = Database.create_delete_query(table_name, key_column_name)
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(query_statement, (delete_id,))
            return True

    @classmethod
    def find(cls, table_name: str, select_column_names: tuple, search_column_name: str, column_value) -> tuple:
        query_statement = Database.create_find_query(table_name, select_column_names, search_column_name)
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(query_statement, (column_value,))
            return cursor.fetchone()

    @classmethod
    def find_all_transactions_with_categories(cls):
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.find_all_transactions)
            return cursor.fetchall()

    @classmethod
    def find_all_categories(cls):
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.find_all_categories)
            return cursor.fetchall()

    @classmethod
    def create_insert_query(cls, table_name, column_names):
        """
        :param table_name: Name of table that's being inserted into
        :param column_names: A tuple of the table's column names
        :return: A valid sql query for inserting a record into the specified database table
        """
        num_of_columns = len(column_names)
        param_list = ['?'] * num_of_columns

        column_string = ", ".join(column_names)
        param_string = ", ".join(param_list)

        return sql_scripts.insert_query.format(table_name=table_name, column_names=column_string, parameters=param_string)

    @classmethod
    def create_find_query(cls, table_name, column_names, key_column_name):
        select_column_names = ", ".join(column_names)
        result = sql_scripts.find_query.format(table_name=table_name, select_column_names=select_column_names,
                                               criteria_column=key_column_name)
        return result

    @classmethod
    def create_update_query(cls, table_name, column_names, primary_key_column_name):
        column_pair_template = "{table_column} = ?"
        column_pairs = [column_pair_template.format(table_column=column_name) for column_name in column_names]
        updated_columns = ", ".join(column_pairs)
        return sql_scripts.update_query.format(table_name=table_name, columns_to_update=updated_columns,
                                               primary_key_column_name=primary_key_column_name)

    @classmethod
    def create_delete_query(cls, table_name, key_column_name):
        return sql_scripts.delete_query.format(table_name=table_name, key_column_name=key_column_name)