from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from application.core import Config

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

app.config.from_object(Config)

db.init_app(app)
