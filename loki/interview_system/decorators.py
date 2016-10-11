def func_args(**kwargs):
    def decorator(func):
        for k, v in kwargs.items():
            setattr(func, k, v)
        return func
    return decorator
