class MetaProvider(type):
    """Метакласс, который кастует в классы моделей менеджера и oauth-клиента"""

    def __new__(cls, name, bases, dct):
        provider_class = super().__new__(cls, name, bases, dct)
        provider_class.manager = provider_class.ManagerConfig.manager(provider_class)
        provider_class.service = provider_class.Config.client
        return provider_class
