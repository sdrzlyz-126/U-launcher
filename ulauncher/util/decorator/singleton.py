from typing import Dict, Any, Callable

CachedInstances = Dict[Any, Any]
objects = {}  # type: CachedInstances


def singleton(fn: Callable) -> Callable:
    """
    Decorator function.
    Call to a decorated function always returns the same instance

    Note: it doesn't take into account args and kwargs when looks up a saved instance
    Call a decorated function with `spawn=True` in order to get a new instance
    """
    def wrapper(*args, **kwargs):
        if not kwargs.get('spawn') and objects.get(fn):
            return objects[fn]

        instance = fn(*args, **kwargs)
        objects[fn] = instance
        return instance

    return wrapper
