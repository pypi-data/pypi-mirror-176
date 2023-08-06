# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvadmin-ak-sk",
    version="1.0.0",
    author="李强",
    author_email="1206709430@qq.com",
    include_package_data=True,
    description="dvadmin-ak-sk 插件是dvadmin的一个ak/sk加密调用插件，使用Access Key Id / Secret Access Key加密的方法来验证某个请求的发送者身份。Access Key Id（AK）用于标示用户，Secret Access Key（SK）是用于加密认证字符串来验证认证字符串的密钥，其中SK必须保密。 AK/SK原理使用对称加解密。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/huge-dream/dvadmin-ak-sk",
    packages=setuptools.find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
