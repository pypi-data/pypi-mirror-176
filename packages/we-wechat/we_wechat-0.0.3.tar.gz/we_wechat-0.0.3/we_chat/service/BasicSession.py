# -*- coding: utf-8 -*-
from rauth.session import RauthSession, OAUTH2_DEFAULT_TIMEOUT
from rauth.compat import urlencode, is_basestring, parse_qsl


class Session(RauthSession):
    __attrs__ = RauthSession.__attrs__ + ['errcode', 'errmsg']

    def __init__(self,
                 service=None,
                 **kwargs):

        for key, value in kwargs.items():
            if key in self.__attrs__:
                setattr(self, key, value)

        super(Session, self).__init__(service)

    def request(self, method, url, **kwargs):
        kwargs.setdefault('params', {})

        url = self._set_url(url)

        kwargs.setdefault('timeout', OAUTH2_DEFAULT_TIMEOUT)

        resp = super(Session, self).request(method, url,
                                            **kwargs)
        if resp.encoding == 'ISO-8859-1':
            resp.encoding = 'utf-8'
        return resp
