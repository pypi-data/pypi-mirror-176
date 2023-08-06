import hashlib
import hmac
import re
import urllib.parse
from random import Random

from .decorators import exceptionHandler


def apiResult(status, code, data='', msg=''):
    return {
        "code": code,
        "data": data,
        "msg": msg,
        "status": status
    }


class CommonUtlis:
    pattern = re.compile("\s+")
    EMPTY_STRING = ""

    @classmethod
    def GetqueryString(cls, parameters):
        """
        获取 queryString 参数
        :param parameters:
        :return:
        """
        sortedKeys = list(parameters)
        if not sortedKeys:
            return ""
        sortedKeys.sort()
        res = ""
        for key in sortedKeys:
            value = cls.__percentEncode(key)
            res = f"{res}&{value}={parameters[key]}"
        return res[1:]

    @classmethod
    def getRandomNum(cls, length):
        r = Random()
        length = 1 if length <= 0 else length
        array = [str(r.randrange(0, 10)) for i in list(range(length))]
        return "".join(array)

    @classmethod
    def getCanonicalQueryString(cls, queryString: str):
        if not queryString:
            return ""
        parameters = dict()
        array = queryString.split("&")
        for param in array:
            keyValue = param.split("=")
            if not keyValue:
                continue
            key = keyValue[0]
            if len(key) == 0:
                parameters[key] = cls.EMPTY_STRING
            else:
                parameters[key] = keyValue[1]
        sortedKeys = list(parameters)
        if not sortedKeys:
            return cls.EMPTY_STRING
        sortedKeys.sort()
        res = ""
        for key in sortedKeys:
            value = cls.__percentEncode(key)
            res = f"{res}&{value}={parameters[key]}"
        return res[1:]

    @classmethod
    def getCanoicalHeader(cls, headerMap: dict):
        signedHeadSet: str = set(headerMap)
        headers = dict()
        for headerName in signedHeadSet:
            value = headerMap.get(headerName)
            if headerName.lower() in ['x-nsf-signature', 'x-nsf-signedheaders']:
                continue
            headers[headerName.lower()] = value
        headerNames = list(headers)
        headerNames.sort()
        # headerNames.sort()
        canonicalHeaders = "".join([f"{headerName}:{cls.trimall(headers[headerName])}\n" for headerName in headerNames])
        return canonicalHeaders

    @classmethod
    def __percentEncode(cls, value: str):
        if not value:
            return value
        return urllib.parse.quote(value, encoding="utf-8")

    @classmethod
    def trimall(cls, value: str):
        if not value:
            return cls.EMPTY_STRING
        return value.strip()
        # return re.sub(cls.pattern, value.strip(), " ")

    @classmethod
    @exceptionHandler(result=None)
    def getHashBodyHex(cls, value: str):
        md = hashlib.sha256()
        if not isinstance(value, bytes):
            value = value.encode(encoding="utf-8")
        md.update(value)
        return md.hexdigest()

    @classmethod
    @exceptionHandler(result="")
    def getSignedHeader(cls, headers: dict):
        signedHeadSet: str = set(headers)
        signedHeaderString = "".join([signedString.lower() + ";" for signedString in signedHeadSet])
        return signedHeaderString[:-1]

    @classmethod
    @exceptionHandler(result="")
    def generateSignature(cls, secret: str, stringToSign: str, algorithm: str = 'SHA256'):
        # algorithm = hashlib.new(algorithm)
        return cls.__hmac(secret.encode('utf-8'), stringToSign.encode('utf-8'), algorithm)

    @classmethod
    def __hmac(cls, secretBytes, stringToSign, algorithm: str):
        signature = hmac.new(secretBytes, stringToSign, digestmod=hashlib.sha256).hexdigest()
        return signature

    @classmethod
    def __HmacSHA256(cls, secretBytes, stringToSign):
        signature = hmac.new(bytes(secretBytes, encoding='utf-8'), bytes(stringToSign, encoding='utf-8'),
                             digestmod=hashlib.sha256).digest()
        return signature.hex().lower()
