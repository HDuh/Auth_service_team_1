import datetime
import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from extensions import db
from models.models_enums import ActionsEnum

__all__ = (
    'AuthHistory',
)


def create_partition(target, connection, **kw) -> None:
    """
    Партиции по браузеру.
    Требуется вручную дублировать в миграциях alembic-а
    """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_chrome" PARTITION OF "auth_history" FOR VALUES IN ('Chrome')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_firefox" PARTITION OF "auth_history" FOR VALUES IN ('Firefox')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_opera" PARTITION OF "auth_history" FOR VALUES IN ('Opera')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_safari" PARTITION OF "auth_history" FOR VALUES IN ('Safari')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_yandex" PARTITION OF "auth_history" FOR VALUES IN ('Yandex')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_unknown" PARTITION OF "auth_history" FOR VALUES IN ('Unknown')"""
    )


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'
    __table_args__ = (
        UniqueConstraint('id', 'browser'),
        {
            'postgresql_partition_by': 'LIST (browser)',
            'listeners': [('after_create', create_partition)],
        }
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(db.String(256))
    action = db.Column(db.Enum(ActionsEnum, name='actions_enum', create_type=False), nullable=False)
    action_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    browser = db.Column(db.String(128), primary_key=True)

    def __repr__(self):
        return f"ID: {self.id}, User ID: {self.user_id}, Action: {self.action}"
