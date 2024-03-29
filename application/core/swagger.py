from api.v1.auth.auth import SignUp, Logout, Refresh, ChangeCredentials, Login
from api.v1.auth.oauth import SocialAuthorize
from api.v1.auth.user import UserProfile, UserAuthHistory
from api.v1.role.role import Roles, RoleList, UserRole


def registration(docs):
    docs.register(SignUp, blueprint='auth')
    docs.register(Login, blueprint='auth')
    docs.register(Logout, blueprint='auth')
    docs.register(Refresh, blueprint='auth')
    docs.register(ChangeCredentials, blueprint='auth')
    docs.register(SocialAuthorize, blueprint='auth')

    docs.register(UserProfile, blueprint='auth')
    docs.register(UserAuthHistory, blueprint='auth')

    docs.register(Roles, blueprint='role')
    docs.register(RoleList, blueprint='role')
    docs.register(UserRole, blueprint='role')
