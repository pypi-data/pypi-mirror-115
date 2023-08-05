import threading


class Singleton(type):
    """Metaclass to create a Singleton."""

    _instance = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instance:
            with Singleton._lock:
                Singleton._instance.setdefault(cls, super().__call__(*args, **kwargs))
        return Singleton._instance[cls]
