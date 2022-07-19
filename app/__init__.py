from flask import Flask
from core.db import init_db, db
from core.config import Config


def create_app():
    # инициализация приложения
    app = Flask(__name__)
    app.config.from_object(Config)

    # инициализация базы данных
    init_db(app)

    # создаем таблицы в БД если нет
    db.create_all(app=app)

    # регистрация blueprints
    from views.auth import auth
    app.register_blueprint(auth, url_prefix='auth/')

    # регистрация моделей
    from models import User

    return app
