from datetime import datetime

__all__ = (
    'expired_time',
    'get_tokens',
)

from flask_jwt_extended import create_access_token, create_refresh_token

from application.models import User


def expired_time(jwt_exp: int) -> int:
    """Вычисление оставшегося времени жизни токена"""

    return round((datetime.fromtimestamp(jwt_exp) - datetime.now()).total_seconds())


def get_tokens(user: User, identity=None) -> tuple:
    """Генерация токенов"""

    access_token = create_access_token(
        identity={
            'user_id': str(user.id),
            'roles': [role.role_name for role in user.role]
        },
        fresh=True
    )
    refresh_token = create_refresh_token(identity=str(user.id) if not identity else identity)
    return access_token, refresh_token
