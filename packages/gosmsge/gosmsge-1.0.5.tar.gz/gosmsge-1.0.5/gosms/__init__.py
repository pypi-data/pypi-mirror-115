from gosms.sms import SMS
from gosms.settings import DEV_URLS, GOSMS_SETTINGS as SETTINGS

try:
    from django.conf import settings as django_settings

    SETTINGS['dev_mode'] = django_settings.DEBUG
    # override dev_mode in GOSMS_SETTINGS in order to use GoSMS.Ge api in development
    try:
        SETTINGS.update(django_settings.GOSMS_SETTINGS)
    except:
        pass

except ModuleNotFoundError:
    """Create gosms manually and pass api_key"""
    pass

sms: SMS = SMS(SETTINGS['api_key'])
