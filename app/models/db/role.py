from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from app.db.db import pg_db
from app.models.db.base import BaseModel, UserIdMixin


class Roles(BaseModel):
    __tablename__ = "roles"

    name = pg_db.Column(pg_db.String(length=64), unique=True, nullable=False)
    permissions = pg_db.Column(pg_db.ARRAY(String), nullable=False)

    def __repr__(self) -> str:
        return f"Role: {self.name} {self.id} {self.permissions}"


class UserSession(UserIdMixin):
    __tablename__ = "user_roles"

    role_id = pg_db.Column(UUID(as_uuid=True), pg_db.ForeignKey("roles.id"))
