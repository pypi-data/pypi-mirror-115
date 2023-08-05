from django.db import models
from django.utils import timezone

from .settings import settings


def _default_notification_dict():
    return {
        'bounces': [],
        'complaints': [],
    }


class EmailAddressNotification(models.Model):
    """ Model to track email notifications. Bounces and complaints.
    """
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=255)

    # Track complaints and bounces
    count = models.PositiveIntegerField(default=0)
    notifications = models.JSONField(default=_default_notification_dict)

    def reset_notification_count(self):
        self.count = 0
        self.save()

    @property
    def email_ok(self):
        return self.count < settings.MAX_COUNT

    def add_notification(self, notification_type, data):
        """ notification_type should be 'bounce' or 'complaint'
            data is the notification dict.
            ref: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/notification-examples.html
        """
        assert(notification_type in ['bounce', 'complaint'])
        self.count += 1
        self.notifications[f'{notification_type}s'].append(data)
        self.save()

    def add_bounce(self, data):
        return self.add_notification('bounce', data)

    def add_complaint(self, data):
        return self.add_notification('complaint', data)
