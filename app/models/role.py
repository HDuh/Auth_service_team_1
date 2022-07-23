import uuid

from sqlalchemy import Column, String, ForeignKey, Text, PickleType

from app.core.db import db

__all__ = (
    'Role',
)


class Role(db.Model):
    __tablename__ = 'role'

    # TODO: PG id надо будет переписать
    id = Column(Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(Text(length=30), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    role_name = Column(String(150), nullable=False)
    permissions = Column(PickleType)
