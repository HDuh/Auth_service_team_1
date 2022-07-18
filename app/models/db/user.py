from sqlalchemy import String

from app.db.db import pg_db
from app.models.db.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    username = pg_db.Column(pg_db.String(length=128), unique=True, nullable=False)
    password = pg_db.Column(pg_db.Text(), nullable=False)
    fullname = pg_db.Column(pg_db.String(length=255), nullable=False)
    mail = pg_db.Column(pg_db.String(length=255), unique=True, nullable=False)
    user_agent = pg_db.Column(pg_db.Text(), nullable=False)
    trusted_devices = pg_db.Column(pg_db.ARRAY(String), nullable=False)
    active = pg_db.Column(pg_db.Boolean(), nullable=False)
    registered_date = pg_db.Column(pg_db.DateTime, default=pg_db.func.now(), nullable=False)
    updated_at = pg_db.Column(pg_db.DateTime, default=pg_db.func.now(), onupdate=pg_db.func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"User: {self.username} {self.id} {self.fullname}"
