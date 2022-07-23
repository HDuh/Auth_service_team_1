import uuid

from sqlalchemy import Column, String

from application.core.db import db

__all__ = (
    'Permission',
)


class Permission(db.Model):
    __tablename__ = 'permission'

    # TODO: PG id надо будет переписать
    id = db.Column(db.Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    permission_name = Column(String(150), nullable=False)
