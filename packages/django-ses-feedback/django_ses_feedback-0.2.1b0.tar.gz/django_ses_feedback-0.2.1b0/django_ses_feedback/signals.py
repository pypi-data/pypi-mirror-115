from django.dispatch import receiver

from django_ses.signals import bounce_received, complaint_received

from .settings import settings
from .models import EmailAddressNotification


def _process_notification(notification_type, obj):
    assert(notification_type in ['bounce', 'complaint'])
    if notification_type == 'bounce':
        obj_var = 'bouncedRecipients'
    else:
        obj_var = 'complainedRecipients'

    for bnc in obj[notification_type][obj_var]:
        _email = bnc['emailAddress'].lower()
        try:
            _en = EmailAddressNotification.objects.get(
                email__iexact=_email,
            )
        except EmailAddressNotification.DoesNotExist:
            _en = EmailAddressNotification(email=_email)
        getattr(_en, f'add_{notification_type}')(obj)  # .save() called here


@receiver(
    bounce_received,
    dispatch_uid='django_ses_feedback.signals.process_bounce',
)
def process_bounce(sender, **kwargs):
    if not settings.PROCESS_BOUNCE:
        return

    _process_notification(
        'bounce',
        {'mail': kwargs['mail_obj'], 'bounce': kwargs['bounce_obj']},
    )


@receiver(
    complaint_received,
    dispatch_uid='django_ses_feedback.signals.process_complaint',
)
def process_complaint(sender, **kwargs):
    if not settings.PROCESS_COMPLAINT:
        return

    _process_notification(
        'complaint',
        {'mail': kwargs['mail_obj'], 'complaint': kwargs['complaint_obj']},
    )
