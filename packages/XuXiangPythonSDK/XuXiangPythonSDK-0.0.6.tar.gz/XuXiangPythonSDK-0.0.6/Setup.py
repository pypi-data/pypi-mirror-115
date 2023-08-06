#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/2/26 3:39 下午
# @Author   : xuxiang
# @Project  : XuXiangPythonLibrary
# @File     : setup.py
# @Software : PyCharm

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XuXiangPythonSDK",
    version="0.0.6",
    author="XuXiang",
    author_email="1456127594@qq.com",
    description="我的自用模块",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/OrlandoXu/XuXiangPythonSDK",
    packages=setuptools.find_packages(),
    install_requires=[
        "apscheduler",
        "pymysql",
        "dbutils",
        "pandas",
        "sqlalchemy",
        "requests",
        "yagmail"

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


