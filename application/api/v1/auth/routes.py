from flask import Blueprint
from flask_restful import Api

from .auth import Login, SignUp, Logout, Refresh, ChangeCredentials
from .oauth import SocialAuthorize, SocialCallback
from .user import UserProfile, UserAuthHistory

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(Logout, '/logout')
api.add_resource(Refresh, '/refresh_token')
api.add_resource(UserProfile, '/user/profile')
api.add_resource(UserAuthHistory, '/user/auth_history')
api.add_resource(ChangeCredentials, '/change_auth_data')
api.add_resource(SocialAuthorize, '/social/auth/<string:provider_name>')
api.add_resource(SocialCallback, '/social/callback/<string:provider_name>')
