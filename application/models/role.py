import uuid

from sqlalchemy.dialects.postgresql import UUID

from application.core.database import db
from .transitional_models import role_permission_table

__all__ = (
    'Role',
)


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name = db.Column(db.String(150), nullable=False)
    permission = db.relationship(
        'Permission',
        secondary=role_permission_table,
        backref='permission',
        lazy='dynamic',
    )
