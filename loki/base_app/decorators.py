from rest_framework.response import Response
from django.core.cache import cache
from functools import wraps

from .helper import split_and_lower


def cache_response(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        cache_key = " ".join(split_and_lower(request.data['query']))
        data = cache.get(cache_key)

        if data is not None:
            print('Query {} found in cache'.format(cache_key))
            print(data)
            return Response(data)

        result = view_func(request, *args, **kwargs)
        cache.set(cache_key, result.data)
        print('Cache miss, setting')

        return result

    return wrapper
