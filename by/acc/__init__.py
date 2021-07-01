import sys

from datetime import date, datetime, timedelta
from acc.services import make_db_connection
from acc.helpers import prompt, input_int, input_date, print_table
from acc import storage


def input_pay():
	"""Запрашивает идентификатор задачи и возвращает ее из БД"""
	def cb(payment_id):
		with make_db_connection() as conn:
			pay = storage.get_payment(conn, int(payment_id))

			if pay is None:
				raise ValueError(f'Товар с ID {task_id} не найден')

			return pay

	return prompt('Введите ID товара', type_cast=cb)



def input_add_payment(pay=None): 
	"""Запрашивает данные от пользователя о задаче и возвращает ввод"""
	pay = dict(pay) if pay else {}
	payment = {}

	payment['title'] = prompt('Наименование товара', default=pay.get('title', '')) 
	payment['price'] = prompt('Цена', default=pay.get('price', 0))
	payment['quantity'] = prompt('Количество', default=pay.get('quantity', 0))
	payment['paydate'] = input_date('Дата', default=pay.get('paydate'))
	payment['availability'] = prompt('Наличие', default=pay.get('availability'))

	return payment


def ac_add_payment():
	# Добавить платеж
	with make_db_connection() as conn:
		payment = input_add_payment()
		storage.create_payment(conn, **payment)
		print(f'''Товар "{payment['title']}" успешно добавлен''')




def ac_edit_payment(): 
	# Отредактировать платеж
	pay = input_pay()

	if pay is not None:
		with make_db_connection() as conn:
			payment = input_add_payment(pay)
			storage.update_payment(conn, pay['id'], **payment)
			print(f'''Товар "{payment['title']}" успешно отредактирован''')



def ac_all_payments():
	# Выводит все платежи
	with make_db_connection() as conn:
		payments = {}
		payments = storage.get_all_payments(conn)
		print_table(
            {
                'id': 'ID',
                'title': 'Наименование товара',
                'price': 'Цена',
                'amount': 'Стоимость',
                'availability': 'Наличие'
            },
            payments
        )



def ac_payments_per_date(): 
	# Выводит все платежи за указанный период
	date_from = input_date('От')
	date_to = input_date('До')

	with make_db_connection() as conn:
		payments = {}
		payments = storage.get_pays_per_date(conn, date_from, date_to)
		print_table(
            {
                'id': 'ID',
                'title': 'Наименование товара',
                'price': 'Цена',
                'amount': 'Стоимость',
                'availability': 'Наличие'
            },
            payments
        )



def ac_large_payments():
	# Выводит топ самых крупных платежей
	top_pos = input_int()
	with make_db_connection() as conn:
		top_payments = storage.get_top_pos(conn, top_pos)
		print_table(
            {
                'id': 'ID',
                'title': 'Наименование товара',
                'price': 'Цена',
                'amount': 'Стоимость',
                'availability': 'Наличие'
            },
            top_payments
        )


def ac_sale_product():
	pay = input_pay()
	avail = input_int('Продано')	

	with make_db_connection() as conn:
		storage.get_sale_product(conn, pay['id'], avail)
		print('Изменения успешно сохранены')	


def ac_menu():
	for num, action in actions.items():
		print(f'{num}. {action[1]}')



def show_usage():
	"""Показать, как исользовать"""

	commads = ', '.join(actions.keys())
	print(f'\nНеизвестная команда.\nВведите одну из: {commands}')



actions = {
	'1': (ac_add_payment, 'Добавить товар'),
	'2': (ac_edit_payment, 'Отредактировать товар'),
	'3': (ac_all_payments, 'Вывести все товары'),
	'4': (ac_payments_per_date, 'Вывести все товары за указанный период'),
	'5': (ac_large_payments, 'Вывести топ самых крупных платежей'),
	'6': (ac_sale_product, 'Проданый товар'),
	'm': (ac_menu, 'Показать меню'),
	'q': (sys.exit, 'Закрыть программу'),
}



def main():
	with make_db_connection() as conn:
		storage.initialize(conn, 'schema.sql')

	ac_menu()

	while True:
		cmd = input('\nВведите команду:	').strip()

		action_tuple = actions.get(cmd, (show_usage, ''))
		action_tuple[0]()






