from application.core.database import db
from .transitional_models import role_permission_table

__all__ = (
    'Permission',
)


class Permission(db.Model):
    __tablename__ = 'permission'

    # TODO: PG id надо будет переписать
    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(150), nullable=False)
    role = db.relationship(
        'Role',
        secondary=role_permission_table,
        backref='role',
        lazy='dynamic',
    )
