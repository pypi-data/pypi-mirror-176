# -*- coding: utf-8 -*-
from rauth.compat import urlencode

from rauth.service import Service

from we_chat.service.settings import api_settings


class BasicService(Service):
    __obj__ = None

    def __init__(
            self,
            appid,
            secret,
            name='wechat',
            access_token_url='https://api.weixin.qq.com/cgi-bin/token',
            authorize_url='https://open.weixin.qq.com/connect/oauth2/authorize',
            base_url='https://api.weixin.qq.com/sns/',
            **kwargs
    ):
        self.appid = appid
        self.secret = secret

        self.access_token_url = access_token_url

        self.base_url = base_url

        for k, v in kwargs.items():
            setattr(self, k, v)

        super(BasicService, self).__init__(name,
                                           base_url,
                                           authorize_url)

    def get_session(self, **kwargs):
        session = self.__obj__(service=self, **kwargs)
        return session

    def get_auth_data(self, api, url, method, **kwargs):
        data = self.get_row_data(api, url, method, **kwargs)
        session = self.get_session(**data)
        return session

    def get_row_data(self, api, url, method, **kwargs):
        params = self.get_params(api=api, **kwargs)
        session = self.get_session()
        r = session.request(method, url, params=params, data=kwargs.get('data'))
        return r.json()

    def get_params(self, api, **kwargs):
        params = getattr(api_settings, api)
        for k, v in params.items():
            if not v:
                params[k] = getattr(self, k)
        for key, value in kwargs.items():
            if value and key != 'data':
                params[key] = value
        return urlencode(params)
