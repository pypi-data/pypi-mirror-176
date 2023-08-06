# -*- coding: utf-8 -*-
from rauth.compat import urlencode

from we_chat.service.BasicService import BasicService
from we_chat.service.BasicSession import Session


class OauthSession(Session):
    """
    认证session类
    """
    __attrs__ = Session.__attrs__ + ['appid',
                                     'secret',
                                     'access_token',
                                     'openid',
                                     'unionid',
                                     ]


class OauthService(BasicService):
    """
    微信小程序服务类
    """

    def __init__(self, appid, secret, phone_number_url="https://api.weixin.qq.com/wxa/business/getuserphonenumber"):
        super(OauthService, self).__init__(appid, secret, phone_number_url=phone_number_url)

    __obj__ = OauthSession

    def get_auth(self, method='GET', api="MINI_ACCESS_TOKEN", **kwargs):
        """
        获取token及openid
        :param api:
        :param method:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.access_token_url, method=method, **kwargs)

    def jscode_login(self, access_token, jscode, method='GET', api="MINI_LOGIN", **kwargs):
        """
        小程序登录获取openid
        :param access_token:
        :param jscode:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(access_token=access_token, api=api, url='jscode2session', jscode=jscode,
                                  method=method, **kwargs)

    def get_phone_number(self, access_token, jscode, method="POST", api="MINI_PHONE_NUMBER", **kwargs):
        """
        获取手机号
        :param access_token:
        :param jscode:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(access_token=access_token, jscode=jscode, api=api, url=self.phone_number_url,
                                  method=method, **kwargs)
