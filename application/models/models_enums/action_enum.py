from enum import Enum

__all__ = (
    'ActionsEnum',
)


class ActionsEnum(Enum):
    SIGNUP = 'signup'
    LOGIN = 'login'
    LOGOUT = 'logout'
    CHANGE_PASSWORD = 'change_password'
    CHANGE_LOGIN = 'change_login'
