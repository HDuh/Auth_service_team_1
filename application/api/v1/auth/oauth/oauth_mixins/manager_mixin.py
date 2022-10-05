from ..provider_manager import ProviderManager

__all__ = (
    'ManagerMixIn',
)


class ManagerMixIn:
    class ManagerConfig:
        manager = ProviderManager
