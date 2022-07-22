import uuid

from flask_login import UserMixin

from app.core.db import db

__all__ = (
    'User',
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    # для PG id надо будет переписать
    id = db.Column(db.Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'
