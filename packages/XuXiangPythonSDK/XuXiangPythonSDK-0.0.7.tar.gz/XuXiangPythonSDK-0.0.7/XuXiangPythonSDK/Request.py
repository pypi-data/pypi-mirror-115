#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/1/21 1:33 下午
# @Author   : xuxiang
# @Project  : XuXiangPythonLibrary
# @File     : Request.py
# @Software : PyCharm

# 网络请求方法

import requests
from requests import adapters
import urllib3
from XuXiangPythonSDK.Log import logger


class Request:
    session = requests.Session()
    session.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 5
    urllib3.disable_warnings()

    # Get请求数据
    # 如果要传入form数据，需要转换成json字符串 data=json.dumps(FormData)
    def getData(self, url, params=None, **kwargs):
        try:
            response = requests.get(url=url, params=params, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error('Get网络请求异常：', e)

    # Post传递表单数据，当前接口的请求类型为application/x-www-form-urlencoded
    # 如果当前请求类型为application/json，仍然想用data传参，需要将字典类型数据转换为json字符串， data=json.dumps(params)
    def postFormData(self, url, data=None, **kwargs):
        try:
            response = requests.post(url=url, data=data, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error('PostFormData异常：', e)


    #  Post传递json数据，当前接口的请求类型为application/json
    def postJsonData(self, url, json=None, **kwargs):
        try:
            response = requests.post(url=url, json=json, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error('PostJsonData异常：', e)








