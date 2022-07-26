from flask_restful import Api

from application.main import app
from application.views.auth import SignUp, Login, Refresh, Logout
from application.views.user import UserProfile, UserAuthHistory

api = Api(app)


def init_api():
    api.add_resource(Login, '/login')
    api.add_resource(SignUp, '/signup')
    api.add_resource(Logout, '/logout')
    api.add_resource(Refresh, '/refresh')
    api.add_resource(UserProfile, '/users/<int:user_id>')
    api.add_resource(UserAuthHistory, '/users/<int:user_id>/auth_history')
