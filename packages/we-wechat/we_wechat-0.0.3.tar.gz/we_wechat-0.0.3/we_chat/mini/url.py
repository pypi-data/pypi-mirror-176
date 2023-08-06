# -*- coding: utf-8 -*-
from we_chat.service.BasicService import BasicService
from we_chat.service.BasicSession import Session


class UrlSession(Session):
    """
    qrcode session类
    """
    __attrs__ = Session.__attrs__ + ['buffer', 'expire_seconds', 'url']


class UrlService(BasicService):
    """
    微信小程序服务类
    """

    def __init__(self,
                 appid,
                 secret,
                 generatescheme_url="https://api.weixin.qq.com/wxa/generatescheme",
                 generate_urllink_url="https://api.weixin.qq.com/wxa/generate_urllink"):
        super(UrlService, self).__init__(appid, secret, generatescheme_url=generatescheme_url,
                                         generate_urllink_url=generate_urllink_url)

    __obj__ = UrlSession

    def generatescheme(self, access_token, post, method='POST', api="DEFAULT_MINI_SCHEME", **kwargs):
        """
        获取 scheme 码
        :param access_token:
        :param post:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.generatescheme_url, access_token=access_token,
                                  method=method, data=post, **kwargs)

    def createwxaqrcode(self, access_token, post, method='POST', api="DEFAULT_MINI_URL", **kwargs):
        """
        获取 URL Link
        :param access_token:
        :param post:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.generate_urllink_url, access_token=access_token,
                                  data=post, method=method, **kwargs)
