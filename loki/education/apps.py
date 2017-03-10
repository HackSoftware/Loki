from django.apps import AppConfig


class EducationConfig(AppConfig):
    name = 'loki.education'
    verbose_name = 'Education'

    def ready(self):
        import loki.education.signals  # noqa
