# -*- coding: utf-8 -*-
from we_chat.service.BasicService import BasicService
from we_chat.service.BasicSession import Session


class QrcodeSession(Session):
    """
    qrcode session类
    """
    __attrs__ = Session.__attrs__ + ['buffer', 'contentType']


class QrcodeService(BasicService):
    """
    微信小程序服务类
    """

    def __init__(self,
                 appid,
                 secret,
                 getwxacodeunlimit_url="https://api.weixin.qq.com/wxa/getwxacodeunlimit",
                 createwxaqrcode_url="https://api.weixin.qq.com/cgi-bin/wxaapp/createwxaqrcode"):

        super(QrcodeService, self).__init__(appid, secret, createwxaqrcode_url=createwxaqrcode_url,
                                            getwxacodeunlimit_url=getwxacodeunlimit_url)

    __obj__ = QrcodeSession

    def getwxacodeunlimit(self, access_token, post, method='POST', api="MINI_QRCODE_LIMIT", **kwargs):
        """
        获取不限制的小程序码
        :param access_token:
        :param post:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.getwxacodeunlimit_url, access_token=access_token,
                                  method=method, data=post, **kwargs)

    def createwxaqrcode(self, access_token, post, method='POST', api="MINI_QRCODE", **kwargs):
        """
        获取小程序二维码
        :param access_token:
        :param post:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.createwxaqrcode_url, access_token=access_token,
                                  data=post, method=method, **kwargs)
