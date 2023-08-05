django-ses-feedback
===================

Simple app to add bounce records to the database. It allows for a helper
to check and see if an email should be delivered to a recipient or not.

Models
~~~~~~

``django_ses_feedback.models.EmailAddressNotification``

Helpers
~~~~~~~

``django_ses_feedback.helpers.can_send_email``

Settings
~~~~~~~~

\``\` SES\ *FEEDBACK = { 'MAX*\ COUNT': 2, 'PROCESS*BOUNCE': True,
'PROCESS*\ COMPLAINT': True, }

\``\`

Notes
~~~~~

This was taken from AnyHow code base for use with other applications.
AnyHow itself doesn't use this because of other model requirements but a
general application should be able to use this just fine.
