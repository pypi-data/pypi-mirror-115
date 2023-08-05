from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    name = 'django_ses_feedback'
    verbose_name = 'Django SES Feedback'

    def ready(self):
        from . import signals
