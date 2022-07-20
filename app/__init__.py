from flask import Flask

from .core.db import init_db, db


def create_app():
    # инициализация приложения
    app = Flask(__name__)
    # app.config.from_object(Config)

    # инициализация базы данных
    init_db(app)


    # регистрация blueprints для auth ручек
    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views.main_page import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # регистрация моделей
    from models import User

    # создаем таблицы в БД если нет
    db.create_all(app=app)
    return app
