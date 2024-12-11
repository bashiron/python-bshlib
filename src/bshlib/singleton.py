class Singleton(type):
    """Generic singleton.

    Inherit by defining it as the metaclass like
    >>> class MyClass(metaclass=Singleton)
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
