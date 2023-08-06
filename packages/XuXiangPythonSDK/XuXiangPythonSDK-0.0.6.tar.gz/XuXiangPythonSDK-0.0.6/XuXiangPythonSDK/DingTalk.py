#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/3/13 3:41 下午
# @Author   : xuxiang
# @Project  : DingTalk
# @File     : DingTalk.py
# @Software : PyCharm

from XuXiangPythonSDK.Request import Request
import time
import urllib.parse
import urllib.request
import hmac
import base64
import hashlib
from XuXiangPythonSDK.Log import logger

class DingTalk:
    # url:创建机器人时生成的Webhook
    # secret:创建机器人时选择加签，生成的秘钥
    def __init__(self, url:str, secret:str=''):
        self.request = Request()

        timestamp = round(time.time()*1000) #时间戳
        secret_enc = secret.encode('utf8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))  # 最终签名


        self.webhook_url = url + '&timestamp={}&sign={}'.format(timestamp, sign)  # 最终url，url+时间戳+签名

    # 发送文本消息
    # msg_content:String 消息内容
    # atAll:Bool 是否@所有人
    # atMobiles:List 被@人的手机号 在content里添加被@人的手机号
    def send_text_msg(self, content, atAll=False, atMobiles=None):

        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype":"text",
            "text":{
                "content":content
            },
            'at':{
                'atMobiles':atMobiles,
                'isAtAll':atAll
            }

        }

        res = self.request.postJsonData(self.webhook_url, json=data, headers=headers)
        if res['errcode'] == 0:
            logger.info('钉钉消息发送成功')
        else:
            logger.error('钉钉消息发送失败',res['errmsg'])

    # 发送链接消息
    # text: String 消息内容
    # title:String 消息标题
    # picUrl:String 图片url
    # messageUrl:String 点击消息跳转的url 以http开头
    # msg_content:String 消息内容
    def send_link_msg(self,title, text, messageUrl, picUrl=None):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "link",
            "link": {
                'text':text,
                'title':title,
                'picUrl':picUrl,
                'messageUrl':messageUrl
            }
        }

        res = self.request.postJsonData(self.webhook_url, json=data, headers=headers)
        if res['errcode'] == 0:
            logger.info('钉钉消息发送成功')
        else:
            logger.error('钉钉消息发送失败', res['errmsg'])

    # 发送markdown消息
    # title:String 列表中展示的消息标题
    # text:String markdown格式的消息
    def send_markdown_msg(self, title, text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "markdown",
            "markdown": {
                'text': text,
                'title': title,
            }
        }

        res = self.request.postJsonData(self.webhook_url, json=data, headers=headers)
        if res['errcode'] == 0:
            logger.info('钉钉消息发送成功')
        else:
            logger.error('钉钉消息发送失败', res['errmsg'])


    # 发送ActionCard消息
    # title:String 列表中展示的消息标题
    # text:String markdown格式的消息
    # singleTitle:String 单个按钮的标题，设置此项和singleURL后btns无效
    # singleUrl:String 点击singleTitle按钮触发的URL
    # btns:List 按钮数组 里面存放{'title': title, 'actionURL': URL}
    # btnOrientation:String 0-按钮竖直排列，1-按钮横向排列
    def send_actionCard_msg(self, title, text, singleTitle=None, singleUrl=None, btns=None, btnOrientation='0'):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "actionCard",
            "actionCard": {
                'text': text,
                'title': title,
                'singleTitle':singleTitle,
                'singleUrl':singleUrl,
                'btn':btns,
                'btnOrientation': btnOrientation
            }
        }

        res = self.request.postJsonData(self.webhook_url, json=data, headers=headers)
        if res['errcode'] == 0:
            logger.info('钉钉消息发送成功')
        else:
            logger.error('钉钉消息发送失败',res['errmsg'])

    # 发送FeedCard消息
    # links:List 存放{'title': title, 'messageURL': messageURL, 'picURL': picURL}
    # title:String 单条消息标题
    # messageURL:String 点击单条消息跳转的链接
    # picURL:String 单条消息的图片URL
    def send_feedCard_msg(self, links):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        data = {
            "msgtype": "feedCard",
            "feedCard": {
                'links': links,

            }
        }

        res = self.request.postJsonData(self.webhook_url, json=data, headers=headers)
        if res['errcode'] == 0:
            logger.info('钉钉消息发送成功')
        else:
            logger.error('钉钉消息发送失败', res['errmsg'])



if __name__ == "__main__":


    msg_content = '啊啊啊'
    text = '这是内容'
    title = '这是标题'
    picUrl = 'https://t7.baidu.com/it/u=3587945189,2578428673&fm=193&f=GIF'
    messageUrl = 'https://www.baidu.com'

    url = 'https://oapi.dingtalk.com/robot/send?access_token=8d6f66b4c8cb1d6a896f6dca8dc41881ac119dc4f17f6a1841b285ac82e6b6b4'
    secret = 'SEC817cca514e4907cc8e7fd01f6c10f36e07ca5132b46bc2b40d082d94ba040770'
    url2= 'https://oapi.dingtalk.com/robot/send?access_token=c55f831c6638003d7d7b2f407354c4b39c673579b399456589ebac626c5ac95f'
    dt = DingTalk(url=url, secret=secret)
    dt.send_link_msg(title=title, text=text, messageUrl=messageUrl)


