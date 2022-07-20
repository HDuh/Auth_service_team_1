import uuid
import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.db import db

__all__ = (
    'User',
)


class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    # для PG id надо будет переписать
    id = db.Column(db.Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean(), default=True, nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)

    # def __init__(self, login, password):
    #     self.login = login
    #     self.password = password
    #
    # def __repr__(self):
    #     return f'<User {self.login}>'
