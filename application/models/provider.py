from sqlalchemy.dialects.postgresql import UUID

from application.extensions import db

__all__ = (
    'Provider',
)


class Provider(db.Model):
    __tablename__ = 'provider'

    id = db.Column(db.Numeric, primary_key=True)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE')
    )
    provider_name = db.Column(db.String(256))
    user = db.relationship(
        'User',
        back_populates='provider'
    )
