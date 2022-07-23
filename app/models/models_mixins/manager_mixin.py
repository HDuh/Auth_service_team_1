from app.models.model_manager import ModelManager

__all__ = (
    'ManagerMixin',
)


class ManagerMixin:
    class ManagerConfig:
        manager = ModelManager
