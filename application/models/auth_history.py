import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from extensions import db
from models.models_enums import ActionsEnum

__all__ = (
    'AuthHistory',
)


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(db.String(256))
    action = db.Column(db.Enum(ActionsEnum, name='actions_enum', create_type=False), nullable=False)
    action_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"ID: {self.id}, User ID: {self.user_id}, Action: {self.action}"
