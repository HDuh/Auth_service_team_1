import uuid

from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Text

from app.core.db import db


__all__ = (
    'UserPermission',
)


# TODO: подумать над uniquely constraint для таблицы
class UserPermission(db.Model, UserMixin):
    __tablename__ = 'user_permission'

    # TODO: PG id надо будет переписать
    id = Column(Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(Text(length=30), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    permission_id = Column(Text(length=30), ForeignKey('permission.id', ondelete="CASCADE"), nullable=False)
