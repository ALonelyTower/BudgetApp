from database import sql_scripts
import settings
from database.database_connection import DatabaseConnection

with DatabaseConnection(settings.DB_PATH) as cursor:
    cursor.execute(sql_scripts.drop_transaction_table_query)
    cursor.execute(sql_scripts.drop_category_table_query)
    cursor.execute(sql_scripts.create_transactions_table_query)
    cursor.execute(sql_scripts.create_categories_table_query)
