import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from dvadmin_ak_sk.client import Auth

AccessKey = '生成的Key'
AccessSecret = '生成的Secret'

AuthObj = Auth(accessKey=AccessKey, accessSecret=AccessSecret)


def get_url(url):
    method = 'GET'
    body = ""
    queryString = ""
    headers = {"content-type": "application/json"}
    res = AuthObj.request(method=method, url=url, headers=headers, body=body, params=queryString)
    print(res)


def post_url(url):
    method = 'POST'
    body = {"name": '测试03', "unique_key": '1111'}
    queryString = ""
    headers = {"content-type": "application/json"}
    res = AuthObj.request(method=method, url=url, headers=headers, body=json.dumps(body), params=queryString)
    print(res)


if __name__ == '__main__':
    get_url('http://127.0.0.1:8000/api/dvadmin_ak_sk/key_manage/')
