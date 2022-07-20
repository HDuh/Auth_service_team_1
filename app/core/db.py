from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import TEST_SQLITE_DB_CONFIG

db = SQLAlchemy()


def init_db(app: Flask):
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@<host>/<database_name>'
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLITE_DB_CONFIG

    # связываем базу данных с приложением
    db.init_app(app)


