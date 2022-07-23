from dataclasses import dataclass
from typing import Any

from app.core.db import db

__all__ = (
    'ModelManager',
)


@dataclass
class ModelManager:
    model: Any

    def save(self):
        db.session.add(self.model)
        db.session.commit()

    def delete(self):
        db.session.delete(self.model)
        db.session.commit()
