import datetime
import uuid

from sqlalchemy import Column, Enum, ForeignKey, DateTime, String, Text

from application.core import db
from application.models.models_enums import ActionsEnum

__all__ = (
    'AuthHistory',
)


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    # TODO: PG id надо будет переписать
    id = db.Column(Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(Text(length=30), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user_agent = Column(String(150))
    action = Column(Enum(ActionsEnum))
    action_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
