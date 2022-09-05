import uuid

from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db
from application.models.models_enums import Genders

__all__ = (
    'Profile',
)


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(Genders))
    phone = db.Column(db.String(15))
    city = db.Column(db.String(128))
    country = db.Column(db.String(128))
    modified_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
