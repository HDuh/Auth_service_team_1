from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from application.core import Config, init_db
from application.views.auth import Login, SignUp, Logout

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
jwt = JWTManager(app)
init_db(app)

api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
