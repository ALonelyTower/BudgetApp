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
    def insert(cls, inserted_data):
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.insert_transaction_query, inserted_data)
            return cursor.lastrowid

    @classmethod
    def update(cls, updated_data):
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.update_transaction_query, updated_data)

            return cursor.lastrowid

    @classmethod
    def delete(cls, delete_id):
        # TODO: Figure out what is returned when deleting a row
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.delete_transaction_query, (delete_id,))
            return True

    @classmethod
    def find(cls, transaction_id):
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.find_transaction_by_id_query, (transaction_id,))
            return cursor.fetchone()

    @classmethod
    def find_all(cls):
        with DatabaseConnection(cls._database_path) as cursor:
            cursor.execute(sql_scripts.find_all_transactions)
            return cursor.fetchall()

