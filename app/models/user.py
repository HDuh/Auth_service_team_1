import datetime
import uuid

from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean, DateTime, Text

from app.models.models_mixins import ManagerMixin
from app.core.db import db

__all__ = (
    'User',
)


class User(db.Model, UserMixin, ManagerMixin):
    __tablename__ = 'user'

    # TODO: PG id надо будет переписать
    id = Column(Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(150))
    last_name = Column(String(150))
    is_active = Column(Boolean(True))
    data_joined = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'
