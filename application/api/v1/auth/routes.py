from flask import Blueprint
from flask_restful import Api

from .auth import Login, SignUp, Logout, Refresh
from .user import UserProfile, UserAuthHistory

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(Logout, '/logout')
api.add_resource(Refresh, '/refresh_token')
api.add_resource(UserProfile, '/user/<string:user_id>')
api.add_resource(UserAuthHistory, '/user/<string:user_id>/auth_history')
