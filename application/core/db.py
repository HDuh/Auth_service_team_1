from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

__all__ = (
    'db',
    'init_db',
)

db = SQLAlchemy()


# инициализация базы данных
def init_db(app: Flask):
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    Migrate(app, db)
