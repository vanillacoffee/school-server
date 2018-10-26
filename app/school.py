# -*- coding: utf-8 -*-
from app import redis
from school_api import SchoolClient
from school_api.session.redisstorage import RedisStorage
from app.utils import service_resp, random_string

session = RedisStorage(redis)


class School(object):

    def __init__(self, url):
        self.school_client = SchoolClient(url, session=session, use_ex_handle=False)

    @service_resp()
    def get_login(self, account, password):
        '''首次登陆验证'''
        self.user = self.school_client.user_login(account, password, use_cookie=False)
        return {"token": random_string(16)}

    @service_resp()
    def get_auth_user(self, account):
        '''使用会话，免密码登陆'''
        auth_user = self.school_client.user_login(account, None)
        return auth_user


class Client(object):
    user_client = None

    @service_resp()
    def get_schedule(self):
        return self.user_client.get_schedule()

    @service_resp()
    def get_score(self):
        return self.user_client.get_score()

    @service_resp()
    def get_info(self):
        return self.user_client.get_info()