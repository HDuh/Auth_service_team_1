from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from application.core import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.init_app(app)

from application.services.permissions import get_access_roles, get_permissions

access_roles = get_access_roles(db)
permissions = get_permissions(db)
api = Api(app)
jwt = JWTManager(app)
