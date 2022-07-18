from app.db.db import pg_db
from app.models.db.base import UserIdMixin


class UserSession(UserIdMixin):
    __tablename__ = "user_session"

    refresh_token = pg_db.Column(pg_db.Text(), nullable=False)
    active = pg_db.Column(pg_db.Boolean(), nullable=False)
    updated_at = pg_db.Column(pg_db.DateTime, default=pg_db.func.now(), onupdate=pg_db.func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"Session: {self.id} {self.updated_at}"


class LoginHistory(UserIdMixin):
    __tablename__ = "login_history"

    action = pg_db.Column(pg_db.String(length=255), nullable=False)
    action_time = pg_db.Column(pg_db.DateTime, default=pg_db.func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"Action: {self.id} {self.action} {self.action_time}"
