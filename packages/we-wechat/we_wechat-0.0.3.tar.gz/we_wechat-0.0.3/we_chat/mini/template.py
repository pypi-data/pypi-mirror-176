# -*- coding: utf-8 -*-
from we_chat.service.BasicService import BasicService
from we_chat.service.BasicSession import Session


class TemplateSession(Session):
    """
    qrcode session类
    """
    __attrs__ = Session.__attrs__ + ['ticket', 'expire_seconds', 'url']


class TemplateService(BasicService):
    """
    微信小程序服务类
    """

    def __init__(self,
                 appid,
                 secret,
                 send_template_url="https://api.weixin.qq.com/cgi-bin/message/subscribe/send"):

        super(TemplateService, self).__init__(appid, secret,
                                              send_template_url=send_template_url)

    __obj__ = TemplateSession

    def send_template_msg(self, access_token, post, method='POST', api="MINI_SEND_TEMPLATE", **kwargs):
        """
        发送订阅消息
        :param access_token:
        :param post:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.send_template_url, access_token=access_token,
                                  data=post, method=method, **kwargs)
