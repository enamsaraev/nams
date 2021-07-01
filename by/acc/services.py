from configparser import ConfigParser
from datetime import datetime 
import sqlite3


def make_config(*config_files):
	"""Читает конфигурационные файлы и возвращает объект ConfigParser"""
	config = ConfigParser()
	config.read(config_files)
	return config


config = make_config('config.ini')


def make_db_connection():
	"""Возвращает объект подключения к БД"""

	db_name = config.get('db', 'db_name')

	conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES) 
	conn.row_factory = sqlite3.Row

	return conn