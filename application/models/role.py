from application.core.database import db
from .transitional_models import role_permission_table

__all__ = (
    'Role',
)


class Role(db.Model):
    __tablename__ = 'role'

    # TODO: PG id надо будет переписать
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(150), nullable=False)
    permission = db.relationship(
        'Permission',
        secondary=role_permission_table,
        backref='permission',
        lazy='dynamic',
    )
