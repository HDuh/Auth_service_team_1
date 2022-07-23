import enum
import uuid

from sqlalchemy import Column, Integer, Enum, ForeignKey, String, DateTime, Text, func

from app.core.db import db

__all__ = (
    'Profile',
)


class Genders(enum.Enum):
    login = 'login'
    logout = 'logout'
    change_password = 'change_password'


class Profile(db.Model):
    __tablename__ = 'profile'

    # TODO: PG id надо будет переписать
    id = Column(Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(Text(length=30), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    age = Column(Integer)
    gender = Column(Enum(Genders))
    phone = Column(String(80))
    city = Column(String(150))
    country = Column(String(150))
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
