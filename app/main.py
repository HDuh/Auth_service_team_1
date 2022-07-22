from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_restful import Api

from app.core.db import init_db
from app.views.auth import Login, SignUp, Logout
from core.config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager().init_app(app)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    init_db(app)
    app.run(debug=True, port=5001)
