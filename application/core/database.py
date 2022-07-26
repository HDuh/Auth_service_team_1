from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from application.main import app

db = SQLAlchemy(app)


# инициализация базы данных
def init_db():
    # db.init_app(app)
    db.create_all()
    # Migrate(app, db)
