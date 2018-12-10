import json


import settings
import sql_scripts
from database_connection import DatabaseConnection


with open(settings.TRANS_FIXTURE_PATH) as json_file:
    trans_fixture = json.load(json_file)

with DatabaseConnection(settings.DB_PATH) as cursor:
    for value in trans_fixture.values():
        query_data = (value['date'], value['category'], value['payment_method'], value['total_expense'],
                      value['description'])
        cursor.execute(sql_scripts.insert_transaction_query, query_data)
