import redis
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from application.core import Config

app = Flask(__name__)
app.config.from_object(Config)
marshmallow = Marshmallow(app)
db = SQLAlchemy(app)

api = Api(app)
jwt = JWTManager(app)
cache = redis.Redis(
    host=Config.CACHE_HOST,
    port=Config.CACHE_PORT,
    db=0,
    decode_responses=True
)
