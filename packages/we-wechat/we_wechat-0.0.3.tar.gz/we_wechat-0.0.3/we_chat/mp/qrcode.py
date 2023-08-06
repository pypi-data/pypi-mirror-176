# -*- coding: utf-8 -*-
from we_chat.service.BasicService import BasicService
from we_chat.service.BasicSession import Session


class QrcodeSession(Session):
    """
    qrcode session类
    """
    __attrs__ = Session.__attrs__ + ['ticket', 'expire_seconds', 'url']


def get_data(action_name, scene_id, scene_str, expire_seconds=None):
    if 'STR' in action_name:
        key = 'scene_str'
        value = scene_str
    else:
        key = 'scene_id'
        value = scene_id
    data = {
        'action_name': action_name,
        'action_info': {
            'scene': {
                key: value
            }
        }
    }
    if expire_seconds:
        data['expire_seconds'] = expire_seconds
    return data


class QrcodeService(BasicService):
    """
    微信公众号服务类
    """

    def __init__(self,
                 appid,
                 secret,
                 qrcode_url="https://api.weixin.qq.com/cgi-bin/qrcode/create",
                 show_qrcode_url="https://mp.weixin.qq.com/cgi-bin/showqrcode"):

        super(QrcodeService, self).__init__(appid, secret, qrcode_url=qrcode_url, show_qrcode_url=show_qrcode_url)

    __obj__ = QrcodeSession

    def get_qrcode_temp(self, access_token, action_name, scene_id, scene_str, expire_seconds=60, method='POST',
                        api="QRCODE_TEMP", **kwargs):
        """
        获取临时二维码
        :param access_token:
        :param action_name:
        :param scene_id:
        :param scene_str:
        :param expire_seconds:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        data = get_data(action_name, scene_id, scene_str, expire_seconds)
        return self.get_auth_data(api=api, url=self.qrcode_url, access_token=access_token,
                                  method=method, data=data, **kwargs)

    def get_qrcode_limit(self, access_token, action_name, scene_id, scene_str, method='POST',
                         api="QRCODE", **kwargs):
        """
        获取长期二维码
        :param access_token:
        :param action_name:
        :param scene_id:
        :param scene_str:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        data = get_data(action_name, scene_id, scene_str)
        return self.get_auth_data(api=api, url=self.qrcode_url, access_token=access_token,
                                  data=data, method=method, **kwargs)

    def show_qrcode(self, ticket, method="GET", api='SHOW_QRCODE', **kwargs):
        """
        根据ticket获取二维码
        :param ticket:
        :param method:
        :param api:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.show_qrcode_url, ticket=ticket, method=method, **kwargs)
