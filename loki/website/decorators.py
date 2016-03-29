from django.contrib.auth.decorators import user_passes_test


def anonymous_required(redirect_url):
    decorator = user_passes_test(
            lambda u: not u.is_authenticated(),
            login_url=redirect_url,
            redirect_field_name=None
    )

    return decorator
