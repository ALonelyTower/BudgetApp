drop_transaction_table_query = """DROP TABLE IF EXISTS transactions"""
drop_category_table_query = """DROP TABLE IF EXISTS categories"""

create_transactions_table_query = """CREATE TABLE IF NOT EXISTS transactions (
                            trans_id INTEGER PRIMARY KEY NOT NULL,
                            trans_date DATE NOT NULL,
                            category_fk INTEGER NOT NULL,
                            trans_payment_method CHAR(50) NOT NULL,
                            trans_total_expense DECIMAL(22, 2) NOT NULL,
                            trans_description VARCHAR(255),
                            FOREIGN KEY (category_fk) REFERENCES categories(cate_id)
                          );"""

create_categories_table_query = """ CREATE TABLE IF NOT EXISTS categories (
                            cate_id INTEGER PRIMARY KEY NOT NULL,
                            cate_name CHAR(50) NOT NULL
                          ); """

insert_query = "INSERT INTO {table_name} ({column_names}) VALUES ({parameters})"

update_query = "UPDATE {table_name} SET {columns_to_update} WHERE {primary_key_column_name} = ?"

find_query = "SELECT * FROM {table_name} WHERE {key_column_name} = ?"

delete_query = "DELETE FROM {table_name} WHERE {key_column_name} = ?"

find_all_transactions = """SELECT trans_id, trans_date, cate_name, trans_payment_method, trans_total_expense, trans_description
                           FROM transactions
                           INNER JOIN categories
                           ON transactions.category_fk_id=categories.cate_id;"""

# TODO: Refactor deprecated queries from project

insert_transaction_query = """INSERT INTO transactions (trans_date, category_fk, trans_payment_method,
                                trans_total_expense,trans_description) VALUES(?,?,?,?,?);"""

insert_category_query = """INSERT INTO categories (cate_name) VALUES(?);"""
