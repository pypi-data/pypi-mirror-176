# -*- coding: utf-8 -*-
DEFAULTS = {
    'DEFAULT_ACCESS_TOKEN': {
        'grant_type': 'authorization_code',
        'appid': None,
        'secret': None,
    },
    'DEFAULT_MINI_LOGIN': {
        'grant_type': 'authorization_code',
        'appid': None,
        'secret': None,
    },
    'DEFAULT_MINI_ACCESS_TOKEN': {
        'grant_type': 'client_credential',
        'appid': None,
        'secret': None,
    },
    'DEFAULT_USER_INFO': {
        'lang': 'zh_CN'
    },
    'DEFAULT_QRCODE_TEMP': {
    },
    'DEFAULT_QRCODE': {
    },
    'DEFAULT_TEMPLATE_LIST': {},
    'DEFAULT_SEND_TEMPLATE': {},
    'DEFAULT_MINI_SEND_TEMPLATE': {},
    'DEFAULT_MINI_QRCODE_LIMIT': {},
    'DEFAULT_MINI_QRCODE': {},
    'DEFAULT_MINI_SCHEME': {},
    'DEFAULT_MINI_URL': {},
}


class APISettings:

    def __init__(self, defaults=None):
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    def __getattr__(self, attr):
        attr = "DEFAULT_" + attr
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)
        val = self.defaults[attr]
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val


api_settings = APISettings(DEFAULTS)
