from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .exception import ArgsErrorException
from .utils import CommonUtlis
from ..models import AkSkManage

User = get_user_model()


class SignatureAuth:
    def __init__(self, request):
        self.request = request
        # 获取到的值存放
        self.MyHeader = {}
        self.canonicalHeader = {}
        self.OtherHeader = {}

    def verify(self, url):
        """
        获取请求头中信息，并判断参数是否合法
        :return:
        """
        # 首先获取X-NSF-SignedHeaders，如果不存在则说明不需要通过网关认证，根据获取到的依次去提取值
        SignedHeaders = self.request.META.get(f"HTTP_{'X-NSF-SignedHeaders'.replace('-', '_').upper()}", "")
        if not SignedHeaders:
            raise ArgsErrorException(code=4000, )  # 请求头错误参数
        # 根据 SignedHeaders 循环取值
        for headerStr in SignedHeaders.split(';'):
            if headerStr == 'content-type':
                self.canonicalHeader[headerStr] = self.request.content_type
                continue
            data = self.request.META.get(f"HTTP_{headerStr.replace('-', '_').upper()}", "")
            if not data:
                raise ArgsErrorException(code=4000,
                                         mes=f"The required input parameter {headerStr} for processing this request is not supplied.")  # 请求头错误参数

            self.canonicalHeader[headerStr] = data
        # body hash加密后串
        try:
            body = self.request.body
        except Exception as e:
            body = b""
        hashBody = CommonUtlis.getHashBodyHex(body)
        # 获取 X-NSF-AccessKey
        AccessKey = self.request.META.get(f"HTTP_{'X-NSF-AccessKey'.replace('-', '_').upper()}", "")
        if not AccessKey:
            raise ArgsErrorException(code=4000,
                                     mes=f"The required input parameter {'X-NSF-AccessKey'} for processing this request is not supplied.")  # 请求头错误参数
        # 根据 AccessKey 去数据库中查询  AccessSecret
        AkSkManage_obj = AkSkManage.objects.filter(access_key=AccessKey, status=1).first()
        if not AkSkManage_obj:
            raise ArgsErrorException(code=4000,
                                     mes=f"Error X-NSF-AccessKey invalid.")  # 请求头错误参数
        # 生成需要加密的 string2Sign
        self.canonicalHeader['host'] = self.request.META.get(f"HTTP_MYHOST", "")
        string2Sign = f"{self.canonicalHeader.get('X-NSF-SignatureMethod'.lower())}\n{self.request.method}" \
                      f"\n{url}\n{CommonUtlis.GetqueryString(self.request.GET)}" \
                      f"\n{CommonUtlis.getCanoicalHeader(self.canonicalHeader)}\n{SignedHeaders}\n{hashBody}"
        # 加密得到 signature
        signature = CommonUtlis.generateSignature(AkSkManage_obj.access_secret, string2Sign, "HmacSHA256")
        # 对比请求传过过来的 signature
        request_signature = self.request.META.get(f"HTTP_{'X-NSF-Signature'.replace('-', '_').upper()}", None)
        if signature != request_signature:
            raise ArgsErrorException(code=4000,
                                     mes=f"The request signature we calculated does not match the signature you provided.")  # 校验失败
        return AccessKey


class AkSkAuthentication(BaseAuthentication):
    """
    access_key、access_secret 认证
    """

    def authenticate(self, request):
        if not request.META.get(f"HTTP_{'X-NSF-SignedHeaders'}".replace('-', '_').upper(), ""):
            return None
        AccessKey = ""
        try:
            AccessKey = SignatureAuth(request).verify(request.META.get(f"HTTP_URL", ""))
        except ArgsErrorException as e:
            if e.code == 4000:
                raise AuthenticationFailed(code=4000, detail=e.mes)
        if AccessKey:
            user = User.objects.filter(ak_sk_manage_user__access_key=AccessKey).first()
            if not user or not user.is_active:
                return None
            return (user, None)
        return None
