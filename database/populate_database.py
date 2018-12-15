import json


import settings
from database import sql_scripts
from database.database_connection import DatabaseConnection


with open(settings.TRANS_FIXTURE_PATH) as json_file:
    transaction_fixture = json.load(json_file)

with open(settings.CATEG_FIXTURE_PATH) as json_file:
    category_fixture = json.load(json_file)

with DatabaseConnection(settings.DB_PATH) as cursor:
    for value in category_fixture.values():
        query_data = (value,)
        cursor.execute(sql_scripts.insert_category_query, query_data)

with DatabaseConnection(settings.DB_PATH) as cursor:
    for value in transaction_fixture.values():
        query_data = (value['date'], value['category'], value['payment_method'], value['total_expense'],
                      value['description'])
        cursor.execute(sql_scripts.insert_transaction_query, query_data)
