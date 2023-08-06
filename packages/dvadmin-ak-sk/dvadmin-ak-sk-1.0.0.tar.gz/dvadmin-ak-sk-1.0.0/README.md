# dvadmin_ak_sk

#### 介绍
dvadmin-ak-sk 插件是dvadmin的一个ak/sk加密调用插件，使用Access Key Id / Secret Access Key加密的方法来验证某个请求的发送者身份。Access Key Id（AK）用于标示用户，Secret Access Key（SK）是用于加密认证字符串来验证认证字符串的密钥，其中SK必须保密。 AK/SK原理使用对称加解密。

#### 软件架构
软件架构说明
## 安装包

使用pip安装软件包：

```python
pip install dvadmin-ak-sk
```


### 方式一: 一键导入注册配置
在 application / settings.py 插件配置中下导入默认配置
```python
...
from dvadmin_ak_sk.settings import *
```
### 方式二: 手动配置
在INSTALLED_APPS 中注册app（注意先后顺序）

```python
INSTALLED_APPS = [
    ...
    'dvadmin_ak_sk',
]
```

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        ...,
        'dvadmin_ak_sk.libs.authentication.AkSkAuthentication'
    )
}
```

在 application / urls.py 中注册url地址
```python
urlpatterns = [
    ...,
    path(r'api/dvadmin_ak_sk/', include('dvadmin_ak_sk.urls')),
]
```


## 使用说明

~~~ python
import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from plugins.dvadmin_ak_sk_backend.client import Auth

AccessKey = 't32fSY09Mi0m0jT2G7XtmG7XgcS6QDzq'
AccessSecret = 'tMAiu8r8eJ4lptxviQ8QHsDOAtNvlG6K'

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
    get_url('http://ip:8000/api/dvadmin_ak_sk/key_manage/')
    # post_url('http://ip.com:8000/api/dvadmin_ak_sk/key_manage/')

~~~
