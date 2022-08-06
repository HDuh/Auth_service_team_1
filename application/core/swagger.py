from application.api.v1.auth.auth import SignUp, Logout, Refresh, ChangeCredentials, Login
from application.api.v1.auth.user import UserProfile, UserAuthHistory
from application.api.v1.role.role import Roles, RoleList, UserRole


def registration(docs):
    docs.register(Login, blueprint='auth')
    docs.register(SignUp, blueprint='auth')
    docs.register(Logout, blueprint='auth')
    docs.register(Refresh, blueprint='auth')
    docs.register(ChangeCredentials, blueprint='auth')

    docs.register(UserProfile, blueprint='auth')
    docs.register(UserAuthHistory, blueprint='auth')

    docs.register(Roles, blueprint='role')
    docs.register(RoleList, blueprint='role')
    docs.register(UserRole, blueprint='role')
