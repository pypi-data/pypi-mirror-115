import functools

from django.db.models.query import Q, QuerySet

from .models import EmailAddressNotification


def can_send_email(email_addresses, clean=True):
    """ Function to take a list of email addresses and return a dictionary
        of email addresses and their notification status. This is to avoid
        emailing addresses that have too many notifications (bounces or
        complaints)

        if clean is True then return a list of all email addresses that
        we're allowed to send email to.
    """
    if not email_addresses:
        return email_addresses

    assert hasattr(email_addresses, "__iter__")
    if isinstance(email_addresses, QuerySet):
        email_addresses = list(email_addresses)
    elif isinstance(email_addresses, str):
        email_addresses = [email_addresses]

    email_addresses = [x.lower() for x in email_addresses]

    # Not using defaultdict because we don't want blanket True's for
    # addresses not present in email_addresses
    ok_emails = {
        x: True for x in list(set([x.lower() for x in email_addresses]))
    }
    q_list = map(lambda x: Q(email__iexact=x), ok_emails.keys())
    q_list = functools.reduce(lambda a, b: a | b, q_list)
    notifications = EmailAddressNotification.objects.filter(q_list).distinct()

    for n in notifications:
        if clean and not n.email_ok:
            del ok_emails[n.email.lower()]
        else:
            ok_emails[n.email.lower()] = n.email_ok

    if clean:
        # This is stupid but needed because tests expect
        # same ordering when comparing recipient lists
        # ok_emails = list(ok_emails.keys())  # keys() returns dict_keys object
        ok_emails = sorted(
            ok_emails.keys(), key=lambda x: email_addresses.index(x),
        )

    return ok_emails
