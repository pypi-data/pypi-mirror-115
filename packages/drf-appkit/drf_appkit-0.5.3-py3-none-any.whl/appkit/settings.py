from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings


USER_SETTINGS = getattr(settings, 'APPKIT', None)

DEFAULTS = {
    'SITEPROFILE_MODEL': '',
}

IMPORT_STRINGS = (
    'SITEPROFILE_MODEL',
)

REMOVED_SETTINGS = (
    'SECRET_KEY',
)


class AppKitSettings(_APISettings):
    def __check_user_settings(self, user_settings):
        pass


appkit_settings = AppKitSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_appkit_settings(*args, **kwargs):  # pragma: no cover
    global appkit_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'APPKIT':
        appkit_settings = AppKitSettings(value, DEFAULTS, IMPORT_STRINGS)

setting_changed.connect(reload_appkit_settings)
