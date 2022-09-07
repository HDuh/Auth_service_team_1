from flask import Blueprint
from flask_restful import Api

from .auth import Login, SignUp, Logout, Refresh, ChangeCredentials
from .social_auth import SocialProvider, GoogleProviderAuth, YandexProviderAuth
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
api.add_resource(SocialProvider, '/social/<string:provider_name>')
api.add_resource(GoogleProviderAuth, '/social/google/auth')
api.add_resource(YandexProviderAuth, '/social/yandex/auth')
