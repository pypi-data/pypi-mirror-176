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
                                     'refresh_token',
                                     'openid',
                                     'unionid']


class OauthService(BasicService):
    """
    微信公众号服务类
    """

    __obj__ = OauthSession

    def get_authorize_url(self, redirect_uri=None, scope='snsapi_base',
                          **params):
        """
        获取微信授权认证URL
        :param redirect_uri: 回调地址
        :param scope: 认证方式 snsapi_base：静默 snsapi_userinfo：获取用户信息
        :param params:
        :return:
        """
        assert redirect_uri
        params.update({'appid': self.appid,
                       'response_type': 'code',
                       'scope': scope,
                       'redirect_uri': redirect_uri})

        query = urlencode(sorted(params.items()))
        return '{0}?{1}#wechat_redirect'.format(self.authorize_url, query)

    def get_auth(self, method='GET', api="ACCESS_TOKEN", **kwargs):
        """
        获取token及openid
        :param api:
        :param method:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.access_token_url, method=method, **kwargs)
