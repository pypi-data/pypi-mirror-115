#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/2/7 9:48 上午
# @Author   : xuxiang
# @Project  : XuXiangPythonLibrary
# @File     : DefaultProgramOpenDirOrFile.py
# @Software : PyCharm

import platform
import os
import subprocess

def openDir(dirPath):
    # 打开文件夹
    if platform.system() == "Windows":
        os.startfile(dirPath)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", dirPath])
    else:
        subprocess.Popen(["xdg-open", dirPath])


def openFile(filePath):
    # 用默认程序打开文件
    if platform.system() == "Windows":
        os.startfile(filePath)
    elif platform.system() == "Darwin":
        subprocess.call(["open", filePath])
    else:
        subprocess.call(["xdg-open", filePath])
