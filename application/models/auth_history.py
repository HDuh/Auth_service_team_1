import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from application.core.database import db
from application.models.models_enums import ActionsEnum

__all__ = (
    'AuthHistory',
)


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(db.String(150))
    action = db.Column(db.Enum(ActionsEnum))
    action_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
