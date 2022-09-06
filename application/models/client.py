from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin
from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db

__all__ = (
    'Client',
)


class Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')
