from configparser import ConfigParser
from datetime import datetime 
import sqlite3


def make_config(*config_files):
	"""Читает конфигурационные файлы и возвращает объект ConfigParser"""
	config = ConfigParser()
	config.read(config_files)
	return config


config = make_config('config.ini')


def make_db_connection(datab):
	"""Возвращает объект подключения к БД"""
	if datab == 1:
		db_name = config.get('db', 'db_name')
	if datab == 2:
		db_name = config.get('db2', 'db_name2')

	conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES) 
	conn.row_factory = sqlite3.Row

	return conn