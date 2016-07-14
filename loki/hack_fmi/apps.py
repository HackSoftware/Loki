from django.apps import AppConfig


class HackFMIConfig(AppConfig):

    name = 'hack_fmi'
    verbose_name = 'Hack FMI'

    def ready(self):

        import hack_fmi.signals.handlers  # noqa
