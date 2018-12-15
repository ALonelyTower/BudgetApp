drop_transaction_table_query = """DROP TABLE IF EXISTS transactions"""
drop_category_table_query = """DROP TABLE IF EXISTS categories"""

create_transactions_table_query = """CREATE TABLE IF NOT EXISTS transactions (
                            trans_id INTEGER PRIMARY KEY NOT NULL,
                            trans_date DATE NOT NULL,
                            category_fk_id INTEGER NOT NULL,
                            trans_payment_method CHAR(50) NOT NULL,
                            trans_total_expense DECIMAL(22, 2) NOT NULL,
                            trans_description VARCHAR(255),
                            FOREIGN KEY (category_fk_id) REFERENCES categories(cate_id)
                          );"""

create_categories_table_query = """ CREATE TABLE IF NOT EXISTS categories (
                            cate_id INTEGER PRIMARY KEY NOT NULL,
                            cate_name CHAR(50) NOT NULL
                          ); """

insert_transaction_query = """INSERT INTO transactions (trans_date, category_fk_id, trans_payment_method,
                                trans_total_expense,trans_description) VALUES(?,?,?,?,?);"""

insert_category_query = """INSERT INTO categories (cate_name) VALUES(?);"""


update_transaction_query = """UPDATE transactions
                              SET trans_date = ?, trans_category = ?, trans_payment_method = ?,
                              trans_total_expense = ?, trans_description = ?
                              WHERE trans_id = ?"""

delete_transaction_query = """DELETE FROM transactions WHERE trans_id = ?"""

find_transaction_by_id_query = "SELECT * FROM transactions WHERE trans_id = (?)"

find_all_transactions = """SELECT trans_id, trans_date, cate_name, trans_payment_method, trans_total_expense, trans_description
                           FROM transactions
                           INNER JOIN categories
                           ON transactions.category_fk_id=categories.cate_id;"""
