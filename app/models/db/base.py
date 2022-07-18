import http
import uuid

from flask_restful import abort
from sqlalchemy.dialects.postgresql import UUID

from app.db.db import pg_db


class BaseModel(pg_db.Model):
    __abstract__ = True

    id = pg_db.Column(UUID(as_uuid=True), nullable=False, unique=True, primary_key=True, default=uuid.uuid4)

    def save_to_db(self):
        try:
            pg_db.session.add(self)
            pg_db.session.commit()
        except BaseException:
            abort(http_status_code=http.HTTPStatus.BAD_REQUEST, message={"message": "Something went wrong"}, )


class UserIdMixin(BaseModel):
    __abstract__ = True

    user_id = pg_db.Column(UUID(as_uuid=True), pg_db.ForeignKey("user.id"))
