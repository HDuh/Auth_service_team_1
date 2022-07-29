from datetime import datetime

__all__ = (
    'expired_time',
)


def expired_time(jwt_exp: int) -> int:
    """Вычисление оставшегося времени жизни токена"""

    return round((datetime.fromtimestamp(jwt_exp) - datetime.now()).total_seconds())
