import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = None

DB_USERNAME = os.getenv('DB_USERNAME', default="ordenes_despacho")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="ordenes_despacho")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="34.121.25.38")


class DatabaseConfigException(Exception):
    def __init__(self, message='Configuration file is Null or malformed'):
        self.message = message
        super().__init__(self.message)


def database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config, dict):
        raise DatabaseConfigException

    if config.get('TESTING', False) == True:
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        return f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/verifica_inventario'


def init_db(app: Flask):
    global db
    db = SQLAlchemy(app)
