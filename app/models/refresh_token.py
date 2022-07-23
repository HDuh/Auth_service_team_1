import datetime
import uuid

from sqlalchemy import Column, ForeignKey, String, DateTime, Text

from app.core.db import db

__all__ = (
    'RefreshToken',
)

token_expired = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)


class RefreshToken(db.Model):
    __tablename__ = 'refresh_token'

    # TODO: PG id надо будет переписать
    id = Column(Text(length=30), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    user_id = Column(Text(length=30), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user_agent = Column(String(150))
    token = Column(String(150))
    # TODO: тут нужно будет использовать константу (время жизни токена),
    #  которую определим в конфигах
    expired = Column(DateTime(timezone=True), default=token_expired)
