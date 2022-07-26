import datetime

from application.core.database import db
from application.models.models_enums import ActionsEnum

__all__ = (
    'AuthHistory',
)


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    # TODO: PG id надо будет переписать
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(db.String(150))
    action = db.Column(db.Enum(ActionsEnum))
    action_time = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
