# -*- coding: utf-8 -*-
from we_chat.service.BasicService import BasicService
from we_chat.service.BasicSession import Session


class UserSession(Session):
    """
    userinfo session类
    """
    __attrs__ = Session.__attrs__ + ['data', 'next_openid', 'total', 'count', 'nickname', 'sex', 'province', 'city',
                                     'country', 'headimgurl', 'unionid']


class UserService(BasicService):
    """
    微信公众号服务类
    """

    def __init__(self,
                 appid,
                 secret,
                 user_list_url="https://api.weixin.qq.com/cgi-bin/user/get"):

        super(UserService, self).__init__(appid, secret, user_list_url=user_list_url)

    __obj__ = UserSession

    def get_userinfo(self, access_token, openid, method='GET', api="USER_INFO", **kwargs):
        """
        获取userinfo
        :param api:
        :param access_token:
        :param openid:
        :param method:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url="userinfo", access_token=access_token,
                                  openid=openid, method=method, **kwargs)

    def get_user_list(self, access_token, next_openid=None, method='GET', api="USER_INFO", **kwargs):
        """
        获取userlist
        :param api:
        :param access_token:
        :param next_openid:
        :param method:
        :param kwargs:
        :return:
        """
        return self.get_auth_data(api=api, url=self.user_list_url, access_token=access_token,
                                  next_openid=next_openid, method=method, **kwargs)
