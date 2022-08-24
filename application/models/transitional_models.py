from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db

__all__ = (
    'user_permission_table',
    'role_permission_table',
    'user_role_table',
)

# Таблица связывает пользователя и разрешения
user_permission_table = db.Table(
    'user_permission',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('permission_id', UUID(as_uuid=True), db.ForeignKey('permission.id')),
)

# Таблица связывает разрешения и роли
role_permission_table = db.Table(
    'role_permission',
    db.Column('permission_id', UUID(as_uuid=True), db.ForeignKey('permission.id')),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id', ondelete='CASCADE')),
)

# Таблица связывает пользователя и роли
user_role_table = db.Table(
    'user_role',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id')),
)
