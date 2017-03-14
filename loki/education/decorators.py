from functools import wraps

from django.core.cache import cache


def cache_result(key_function):
    def inner(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            key = key_function(*args, **kwargs)
            cached_result = cache.get(key)
            """
            cached_result is float value and cannot be evaluated as True or False
            """
            if cached_result is None:
                cached_result = function(*args, **kwargs)
                cache.set(key, cached_result)
            return cached_result
        return wrapper
    return inner
