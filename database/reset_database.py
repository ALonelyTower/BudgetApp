import settings


from database import sql_scripts
from database.database_connection import DatabaseConnection


def reset_database(database_path):
    with DatabaseConnection(database_path) as cursor:
        cursor.execute(sql_scripts.drop_transaction_table_query)
        cursor.execute(sql_scripts.drop_category_table_query)
        cursor.execute(sql_scripts.create_transactions_table_query)
        cursor.execute(sql_scripts.create_categories_table_query)


if __name__ == '__main__':
    reset_database(settings.DB_PATH)
