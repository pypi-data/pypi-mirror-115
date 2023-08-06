#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/2/4 3:44 下午
# @Author   : xuxiang
# @Project  : XuXiangPythonLibrary
# @File     : FileReadWrite.py
# @Software : PyCharm

class FileReadWrite:
    # mode
    # r 只读，不能创建文件
    # r+ 读写，不能创建文件，写入时插入到原有内容开头，会从头覆盖部分原有内容，覆盖长度和新写入的内容相同
    # rb，只读，不能创建文件，以二进制读取
    # w 只写，可以创建文件，写入会全部覆盖原有内容
    # wb 只写，可以创建文件，写入会全部覆盖原有内容，以二进制写入
    # a 追加写入，可以创建文件，写入时追加到原有内容后面
    # ab 追加写入，可以创建文件，写入时追加到原有内容后面，以二进制写入



    def __init__(self, file, mode):

        try:
            self.file = open(file=file, mode=mode)

        except Exception as e:
            print('以{}模式打开文件{}出错，原因：{}'.format(mode,file, e))


    # 读取文件
    def read(self):
        return self.file.read()

    # 写入文件
    def write(self, content):
        self.file.write(content)

    # 关闭文件
    def close(self):
        self.file.close()





