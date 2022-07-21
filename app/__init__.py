import os

from flask import Flask
from dotenv import load_dotenv
from .core.db import init_db, db
from flask_login import LoginManager

load_dotenv()


def create_app():
    # инициализация приложения
    app = Flask(__name__)
    # app.config.from_object(Config)

    # инициализация базы данных
    init_db(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # регистрация blueprints для auth ручек
    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views.main_page import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # регистрация моделей
    from models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # создаем таблицы в БД если нет
    db.create_all(app=app)
    return app
