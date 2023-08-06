import datetime
import json
import logging

import requests
from rest_framework.request import Request

from application import settings
from ..common.exception import ArgsErrorException
from ..common.utils import CommonUtlis, CommonParams

logger = logging.getLogger(__file__)


class Auth:

    def __init__(self, accessKey, accessSecret, tenant_name=None):
        if getattr(settings, 'PLUGINS_LIST', {}).get('dvadmin_tenant_backend', None) and tenant_name:
            from django_tenants.utils import schema_context
            from dvadmin_ak_sk.models import AkSkManage
            from django.db import connection
            with schema_context("public"):
                obj = AkSkManage.objects.filter(user__username=tenant_name, status=1).first()
                if obj:
                    accessKey = obj.access_key
                    accessSecret = obj.access_secret
        self.dryOn = 'false'
        self.accessKey = accessKey
        self.accessSecret = accessSecret

    def getSignedHeader(self, headerMap: dict):
        if not self.checkHeaders(headerMap):
            raise ArgsErrorException("401", "Error Parameter of header")
        return CommonUtlis.getSignedHeader(headerMap)

    def getSignatureHeader(self, dryOn: str = "false", accessKey: str = "", accessSecret: str = "",
                           host: str = "", httpMethod: str = "", url: str = "", queryString: str = "",
                           body="", headers: dict = None):
        if not headers:
            headers = dict()
        headers[CommonParams.X_NSF_SIGNATURE_METHOD] = CommonParams.SIGNATURE_METHOD
        headers[CommonParams.X_NSF_SIGNATURE_VERSION] = CommonParams.SIG_VERSION_V1
        headers[CommonParams.X_NSF_DryRun] = dryOn
        headers["URL"] = url
        headers[CommonParams.X_NSF_SIGNATURE_NONCE] = CommonUtlis.getRandomNum(64)  # 随机64 位数
        headers[CommonParams.X_NSF_AccessKey] = accessKey
        # 获取时间 格式为 %Y-%m-%dT%H:%M:%SZ
        headers[CommonParams.X_NSF_DATE] = datetime.datetime.utcnow().strftime(CommonParams.ISO8601_DATE_TIME_FORMATTER)
        host = host.split(":")[0]
        headers[CommonParams.HOST] = host
        canonicalQueryString = CommonUtlis.getCanonicalQueryString(queryString)
        canonicalHeader = CommonUtlis.getCanoicalHeader(headers)
        signedHeader = CommonUtlis.getSignedHeader(headers)
        headers[CommonParams.X_NSF_SIGNED_HEADERS] = signedHeader
        hashBody = CommonUtlis.getHashBodyHex(body)
        string2Sign = f"{CommonParams.SIGNATURE_METHOD}\n{httpMethod}\n{url}\n{canonicalQueryString}\n{canonicalHeader}\n{signedHeader}\n{hashBody}"
        signature = CommonUtlis.generateSignature(accessSecret, string2Sign, "HmacSHA256")
        headers[CommonParams.X_NSF_SIGNATURE] = signature
        headers["MYHOST"] = host
        return headers

    def checkHeaders(self, headerMap: dict):
        return set(headerMap).issuperset(CommonParams.StandardardHeader)

    def GetHeader(self):
        """
        加密获取请求头信息
        :return:
        """
        url = '/' + "/".join(self.url.split('/')[3:])
        return self.getSignatureHeader(dryOn=self.dryOn, accessKey=self.accessKey,
                                       accessSecret=self.accessSecret,
                                       host=self.host, httpMethod=self.httpMethod, url=url,
                                       queryString=self.queryString,
                                       body=self.body, headers=self.headers)

    def request(self, method, url, params="", body="", headers={"content-type": "application/json"}, timeout=10):
        if not isinstance(body, str):
            body = json.dumps(body)
        if not isinstance(params, str):
            params = json.dumps(params)
        self.url = url
        self.queryString = params
        self.headers = headers
        self.body = body
        self.host = url.split('/')[2]
        self.httpMethod = method
        self.request_headers = self.GetHeader()
        dic = {'url': url, 'data': self.body, 'headers': self.request_headers, 'params': self.queryString,
               'timeout': timeout}
        if self.httpMethod == "POST":
            res = requests.post(**dic)
        elif self.httpMethod == "DELETE":
            res = requests.delete(**dic)
        elif self.httpMethod == "PUT":
            res = requests.put(**dic)
        else:
            res = requests.get(**dic)
        try:
            content = json.loads(res.content.decode('utf-8'))
        except Exception as e:
            content = res.content
        return content
