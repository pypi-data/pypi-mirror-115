from django.conf import settings as django_settings


_settings = {
    'MAX_COUNT': 2,
    'PROCESS_BOUNCE': True,
    'PROCESS_COMPLAINT': True,
}


class Settings(object):
    def __getattribute__(self, name):
        sdict = getattr(django_settings, 'SES_FEEDBACK', {})
        return sdict.get(name, _settings.get(name))


settings = Settings()
