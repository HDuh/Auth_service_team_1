import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from extensions import db
from .transitional_models import user_permission_table, user_role_table

__all__ = (
    'User',
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean(True))
    data_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    profile = db.relationship('Profile', backref='user', uselist=False)
    auth_history = db.relationship('AuthHistory', backref='user', lazy='dynamic')

    permission = db.relationship(
        'Permission',
        secondary=user_permission_table,
        backref='user',
        lazy='dynamic',
    )
    role = db.relationship(
        'Role',
        secondary=user_role_table,
        backref='user',
        lazy='dynamic',
    )

    def __repr__(self):
        return f'<User {self.email}>'

    def get_id(self):
        return str(self.id)
