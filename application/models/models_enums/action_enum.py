from enum import Enum

__all__ = (
    'ActionsEnum',
)


class ActionsEnum(Enum):
    signup = 'signup'
    login = 'login'
    logout = 'logout'
    change_password = 'change_password'
