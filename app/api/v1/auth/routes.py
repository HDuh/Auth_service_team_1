from . import api
from .security import ChangePassword
from .login import UserLogin, UserLogout
from .token import TokenRefresh
from .user_profile import Profile, GetHistory
from .registration import UserRegistration

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(Profile, '/user')
api.add_resource(GetHistory, '/access_history')
api.add_resource(ChangePassword, '/change_password')
