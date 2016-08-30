from django.apps import AppConfig


class BaseAppConfig(AppConfig):

    name = 'loki.base_app'
    verbose_name = 'BaseApp'

    def ready(self):
        pass
