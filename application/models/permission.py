import uuid

from sqlalchemy.dialects.postgresql import UUID

from application.core.database import db
from .transitional_models import role_permission_table

__all__ = (
    'Permission',
)


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_name = db.Column(db.String(150), nullable=False)
    role = db.relationship(
        'Role',
        secondary=role_permission_table,
        backref='role',
        lazy='dynamic',
    )
