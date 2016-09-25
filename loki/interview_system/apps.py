from django.apps import AppConfig


class InterviewSystemConfig(AppConfig):
    name = 'loki.interview_system'

    def ready(self):
        import loki.interview_system.signals # noqa
