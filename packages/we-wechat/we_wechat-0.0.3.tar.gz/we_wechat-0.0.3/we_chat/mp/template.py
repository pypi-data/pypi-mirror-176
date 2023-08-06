# -*- coding: utf-8 -*-
from we_chat.service.BasicService import BasicService
from we_chat.service.BasicSession import Session


class TemplateSession(Session):
    """
    qrcode session类
    """
    __attrs__ = Session.__attrs__ + ['template_list']


class TemplateService(BasicService):
    """
    微信公众号服务类
    """

    def __init__(self,
                 appid,
                 secret,
                 template_list_url="https://api.weixin.qq.com/cgi-bin/template/get_all_private_template",
                 send_template_url="https://api.weixin.qq.com/cgi-bin/message/template/send"):

        super(TemplateService, self).__init__(appid, secret, template_list_url=template_list_url,
                                              send_template_url=send_template_url)

    __obj__ = TemplateSession

    def get_template_list(self, access_token, method='GET', api="TEMPLATE_LIST", **kwargs):
        """
        获取模板消息列表
        :param access_token:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.template_list_url, access_token=access_token,
                                  method=method, **kwargs)

    def send_template_msg(self, access_token, post, method='POST', api="SEND_TEMPLATE", **kwargs):
        """
        发送模板消息
        :param access_token:
        :param post:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.send_template_url, access_token=access_token,
                                  data=post, method=method, **kwargs)
