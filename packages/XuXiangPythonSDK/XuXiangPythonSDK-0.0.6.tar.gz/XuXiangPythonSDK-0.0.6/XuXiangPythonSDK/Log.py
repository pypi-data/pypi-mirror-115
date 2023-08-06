#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/7/6 10:33 上午
# @Author   : xuxiang
# @Project  : 报表
# @File     : Log.py
# @Software : PyCharm

import logging
import sys
import os
# from logging.handlers import HTTPHandler
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# StreamHandler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
stream_formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)

# FileHandler
# file_handler = logging.FileHandler('报表日志.log')
# file_handler.setLevel(level=logging.INFO)
# file_formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)

# RotatingFileHandler
path = os.getcwd()+'/报表日志'
if not os.path.exists(path):
    os.makedirs(path)
rotating_file_handler = RotatingFileHandler('报表日志/报表日志.log', maxBytes=1024*1024, backupCount=3)
rotating_file_handler.setLevel(level=logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
rotating_file_handler.setFormatter(file_formatter)
logger.addHandler(rotating_file_handler)


# HTTPHandler
# 需要先启动HTTP Server并运行在8001端口
# http_handler = HTTPHandler(host='localhost:8001', url='log', method='POST')
# http_handler.setLevel(level=logging.INFO)
# logger.addHandler(http_handler)







