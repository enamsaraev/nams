import sys

from datetime import date, datetime, timedelta
from acc.services import make_db_connection
from acc.helpers import prompt, input_int, input_date, print_table
from acc import storage


def input_pay():
	"""Запрашивает идентификатор задачи и возвращает ее из БД"""
	def cb(payment_id):
		with make_db_connection(1) as conn:
			pay = storage.get_payment(conn, int(payment_id))

			if pay is None:
				raise ValueError(f'Товар с ID {task_id} не найден')

			return pay

	return prompt('Введите ID товара', type_cast=cb)


def input_pay_id(pr_id=None):
	with make_db_connection(1) as conn:
			pay = storage.get_payment(conn, int(pr_id))

			if pay is None:
				raise ValueError(f'Товар с ID {task_id} не найден')

			return pay


def input_add_product(pay=None): 
	"""Запрашивает данные от пользователя о задаче и возвращает ввод"""
	pay = dict(pay) if pay else {}
	payment = {}

	payment['title'] = prompt('Наименование товара', default=pay.get('title', '')) 
	payment['price'] = prompt('Цена', default=pay.get('price', 0))
	payment['quantity'] = prompt('Количество', default=pay.get('quantity', 0))
	payment['paydate'] = input_date('Дата', default=pay.get('paydate'))

	return payment


def add_more_products(pr=None):
	pr = dict(pr) if pr else {}
	product = {}

	product['price'] = prompt('Цена', default=pr.get('price', 0))
	product['quantity'] = prompt('Количество', default=0)
	product['paydate'] = input_date('Дата', default=0)	

	return product


def add_sold_product():
	product = {}

	product['title'] = prompt('Наименование товара')
	product['sold'] = prompt('Количество')
	product['soldprice'] = prompt('Цена')
	product['prdate'] = input_date('Дата')

	return product


def ac_add_product():
	# Добавить товар
	with make_db_connection(1) as conn:
		product = input_add_product()
		storage.create_payment(conn, **product)
		print(f'''Товар "{product['title']}" успешно добавлен''')


def ac_edit_product(): 
	# Добавить новое поступление товара
	pr = input_pay()

	if pr is not None:
		with make_db_connection(1) as conn:
			product = add_more_products(pr)
			storage.update_payment(conn, pr['id'], **product)
			print(f'''Товар "{pr['title']}" успешно отредактирован''')



def ac_all_products():
	# Выводит все товары
	with make_db_connection(1) as conn:
		products = {}
		products = storage.get_all_payments(conn)
		print_table(
            {
                'id': 'ID',
                'title': 'Наименование товара',
                'price': 'Цена',
                'amount': 'Стоимость',
                'availability': 'Наличие'
            },
            products
        )



def ac_products_per_date(): 
	# Выводит все товары за указанный период
	date_from = input_date('От')
	date_to = input_date('До')

	with make_db_connection(1) as conn:
		products = {}
		products = storage.get_pays_per_date(conn, date_from, date_to)
		print_table(
            {
                'id': 'ID',
                'title': 'Наименование товара',
                'price': 'Цена',
                'amount': 'Стоимость',
                'availability': 'Наличие'
            },
            products
        )



def ac_large_products():
	# Выводит топ самых крупных товароы
	top_pos = input_int()
	with make_db_connection(1) as conn:
		top_products = storage.get_top_pos(conn, top_pos)
		print_table(
            {
                'id': 'ID',
                'title': 'Наименование товара',
                'price': 'Цена',
                'amount': 'Стоимость',
                'availability': 'Наличие'
            },
            top_products
        )


def ac_sale_product():
	# Проданный товар
	
	pr = add_sold_product()

	with make_db_connection(1) as conn:
		storage.get_sale_product(conn, pr['title'], pr['sold'])	
	
	with make_db_connection(2) as conn:
		storage.set_sold_product(conn, pr.get('title'), pr.get('sold'), pr.get('soldprice'), pr.get('prdate'))
	


def ac_sold_products():
	pr = input('Наименование:  ')

	with make_db_connection(2) as conn:
		product = {}
		product = storage.get_sold_product(conn, pr)
		print_table(
			{
				'id': 'ID',
                'title': 'Наименование товара',
                'sold': 'Количество',
                'soldprice': 'Стоимость',
                'prdate': 'Дата'
			},
			product
		)	


def ac_menu():
	for num, action in actions.items():
		print(f'{num}. {action[1]}')



def show_usage():
	"""Показать, как исользовать"""

	commads = ', '.join(actions.keys())
	print(f'\nНеизвестная команда.\nВведите одну из: {commands}')



actions = {
	'1': (ac_add_product, 'Добавить новый товар'),
	'2': (ac_edit_product, 'Добавить товар'),
	'3': (ac_all_products, 'Вывести все товары'),
	'4': (ac_products_per_date, 'Вывести все товары за указанный период'),
	'5': (ac_large_products, 'Вывести топ самых крупных платежей'),
	'6': (ac_sale_product, 'Проданый товар'),
	'7': (ac_sold_products, 'Отчет по проданному товару'),
	'm': (ac_menu, 'Показать меню'),
	'q': (sys.exit, 'Закрыть программу'),
}



def main():
	with make_db_connection(1) as conn:
		storage.initialize(conn, 'schema.sql')

	with make_db_connection(2) as conn:
		storage.initialize(conn, 'schema2.sql')

	ac_menu()

	while True:
		cmd = input('\nВведите команду: ').strip()

		action_tuple = actions.get(cmd, (show_usage, ''))
		action_tuple[0]()






