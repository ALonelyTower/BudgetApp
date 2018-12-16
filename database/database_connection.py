import sqlite3
import settings
from database import sql_scripts
from sqlite3 import DatabaseError


class DatabaseConnection:
    def __init__(self, database_path):
        if database_path is None:
            raise TypeError("Database path must be set prior to access.")

        try:
            self._database_connection = sqlite3.connect(database_path)
        except DatabaseError as db_e:
            print(f"Error occurred in connecting to database: {db_e}")
            print(f"Database path given: {database_path}")

    def __enter__(self):
        return self._database_connection.cursor()

    def __exit__(self, except_type, except_value, traceback):
        if traceback is None:
            self._database_connection.commit()
            self._database_connection.close()
        else:
            self._database_connection.rollback()
            raise except_type(except_value)


class Database:
    _database_path = settings.DB_PATH

    def __init__(self):
        pass

    @classmethod
    def insert(cls, table_name, column_names, table_values):
        query_statement = Database.create_insert_query(table_name, column_names)
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(query_statement, table_values)
            return cursor.lastrowid

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
    def find(cls, table_name, key_column_name, record_id):
        query_statement = Database.create_find_query(table_name, key_column_name)
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(query_statement, (record_id,))
            return cursor.fetchone()

    @classmethod
    def find_all(cls):
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.find_all_transactions)
            return cursor.fetchall()

    @classmethod
    def create_insert_query(cls, table_name, column_names):
        """
        :param table_name: Name of database table that's being inserted into
        :param column_names: A tuple of the table's column names
        :return: A valid sql query for inserting a record into the specified database table
        """
        num_of_columns = len(column_names)
        param_list = ['?'] * num_of_columns

        column_string = ", ".join(column_names)
        param_string = ", ".join(param_list)

        return sql_scripts.insert_query.format(table_name=table_name, column_names=column_string, parameters=param_string)

    @classmethod
    def create_find_query(cls, table_name, key_column_name):
        return sql_scripts.find_query.format(table_name=table_name, key_column_name=key_column_name)

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
