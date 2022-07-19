import uuid

from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import db

__all__ = (
    'User',
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    email = Column(String(150), unique=True)
    first_name = Column(String(150))
    last_name = Column(String(150))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<User {self.login}>'
