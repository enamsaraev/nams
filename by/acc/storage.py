from datetime import datetime, time



SQL_CREATE_NEW_PAYMENT = 'INSERT INTO payment_table (title, price, quantity, paydate) VALUES (?, ?, ?, ?)'

SQL_UPDATE_PAYMENT = 'UPDATE payment_table SET price=?, quantity=?, paydate=? WHERE id=?'

SQL_SELECT_ALL_PAYMENTS = 'SELECT id, title, price, amount, availability FROM payment_table'

SQL_SELECT_PAYMENTS_PER_DATE = f'{SQL_SELECT_ALL_PAYMENTS} WHERE paydate BETWEEN ? AND ?'

SQL_SELECT_LARGE_PAYMENTS = f'{SQL_SELECT_ALL_PAYMENTS} WHERE price=?'

SQL_SELECT_PAYMENT_BY_ID = f'{SQL_SELECT_ALL_PAYMENTS} WHERE id=?'



def initialize(conn, creation_schema):
	"""Используя переданный SQL-скрипт инициализирует структуру БД"""
	with open(creation_schema) as f:
		conn.executescript(f.read())



def create_payment(conn, title, price, quantity, paydate):
	"""Сохраняет новый платеж в БД."""
	conn.execute(SQL_CREATE_NEW_PAYMENT, (title, price, quantity, paydate))
	conn.execute('UPDATE payment_table SET amount = price*quantity') 
	conn.execute('UPDATE payment_table SET availability = quantity') 



def update_payment(conn, pr_id, price, quantity, paydate):
	"""Обновляет платеж в БД"""
	conn.execute(SQL_UPDATE_PAYMENT, (price, quantity, paydate, pr_id))
	conn.execute('UPDATE payment_table SET availability=availability+quantity WHERE id=?', (pr_id,))
	conn.execute('UPDATE payment_table SET amount = price*availability WHERE id=?', (pr_id,))



def get_payment(conn, payment_id):
	"""Возвращает ID платежа"""
	return conn.execute(SQL_SELECT_PAYMENT_BY_ID, (payment_id,)).fetchone()



def get_all_payments(conn):
	"""Выбирает и возвращает все платежи"""
	return conn.execute(SQL_SELECT_ALL_PAYMENTS).fetchall()
	


def get_pays_per_date(conn, date_from, date_to):
	"""Возвращает платежи за указанный период"""
	return conn.execute(SQL_SELECT_PAYMENTS_PER_DATE, (date_from, date_to)).fetchall()



def get_large_payments(conn, price):
	"""Возвращает самые крупные платежи из БД"""
	return conn.execute(SQL_SELECT_ALL_TASKS, (amount,)).fetchall()



def get_top_pos(conn, top_pos):
	"""Возвращает кол-во платежей в топе"""
	return conn.execute('SELECT  id, title, price, quantity, availability, amount FROM payment_table ORDER BY amount DESC LIMIT ?', [top_pos]).fetchall()


def get_sale_product(conn, pr_title, availability_product):
	conn.execute('UPDATE payment_table SET availability=availability-? WHERE title=?', (availability_product, pr_title))
	conn.execute('UPDATE payment_table SET amount=price*availability WHERE title=?', (pr_title,))


def set_sold_product(conn, title, pr_sold, pr_soldprice, pr_date):
	conn.execute('INSERT INTO payment_table2 (title, sold, soldprice, prdate) VALUES (?, ?, ?, ?)', (title, pr_sold, pr_soldprice, pr_date))
	conn.execute('UPDATE payment_table2 SET soldprice=soldprice*sold WHERE id=MAX')

def get_sold_product(conn, title):
	return conn.execute('SELECT id, title, sold, soldprice, prdate FROM payment_table2 WHERE title=?', (title,)).fetchall()






