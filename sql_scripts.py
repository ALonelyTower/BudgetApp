drop_transaction_table_query = """DROP TABLE IF EXISTS transactions"""

create_transaction_table_query = """CREATE TABLE IF NOT EXISTS transactions (
                            trans_id INTEGER PRIMARY KEY NOT NULL,
                            trans_date DATE NOT NULL,
                            trans_category CHAR(50) NOT NULL,
                            trans_payment_method CHAR(50) NOT NULL,
                            trans_total_expense DECIMAL(22, 2) NOT NULL,
                            trans_description VARCHAR(255)
                            );"""

insert_transaction_query = """INSERT INTO transactions (trans_date,trans_category,trans_payment_method,
                                trans_total_expense,trans_description) VALUES(?,?,?,?,?);"""


update_transaction_query = """UPDATE transactions
                              SET trans_date = ?, trans_category = ?, trans_payment_method = ?,
                              trans_total_expense = ?, trans_description = ?
                              WHERE trans_id = ?"""

delete_transaction_query = """DELETE FROM transactions WHERE trans_id = ?"""

find_transaction_by_id_query = "SELECT * FROM transactions WHERE trans_id = (?)"

find_all_transactions = "SELECT * FROM transactions"
