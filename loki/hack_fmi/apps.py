from django.apps import AppConfig


class HackFMIConfig(AppConfig):

    name = 'loki.hack_fmi'
    verbose_name = 'Hack FMI'

    def ready(self):
        import loki.hack_fmi.signals
