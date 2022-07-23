__all__ = (
    'MetaModel',
)


class MetaModel(type):
    def __new__(cls, name, bases, dct):
        model_class = super().__new__(cls, name, bases, dct)
        model_class.manager = model_class.ManagerConfig.manager(model_class)
        return model_class
