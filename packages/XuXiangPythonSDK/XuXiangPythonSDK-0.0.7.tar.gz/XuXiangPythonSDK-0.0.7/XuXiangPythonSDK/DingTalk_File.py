#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/3/24 3:24 下午
# @Author   : xuxiang
# @Project  : PythonProjects
# @File     : DingTalk2.0.py
# @Software : PyCharm

from XuXiangPythonSDK.Request import Request



class DingTalk2():
    def __init__(self, appkey, appsecret):
        self.request = Request()
        self.appkey = appkey
        self.appsecret = appsecret
        self.access_token = self.getAccess_token()

    def getAccess_token(self):
        url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (self.appkey, self.appsecret)

        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        data = {'appkey': appkey,
                'appsecret': appsecret}
        res = self.request.getData(url=url, data=data, headers=headers)
        if res['errcode'] == 0:
            return res['access_token'] #'d258a449d3c831e783acb7db0126be96'
        else:
            print('token获取失败')
            return None



    # 上传文件，获取media_id
    # filePath 文件路径
    def getMedia_id(self, filePath):  # 拿到接口凭证
        url = 'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % self.access_token
        files = {'media': open(filePath, 'rb')}
        data = {'access_token': self.access_token,
                'type': 'file'}

        res = self.request.postFormData(url=url, files=files, data=data)

        if res['errcode'] == 0:
            return res["media_id"]
        else:
            print('获取medie_id失败')
            return None

    # 发送文件到指定群
    # filePath 文件路径
    # chatId 群id 通过jsapi工具获取的群聊id  https://wsdebug.dingtalk.com/
    def SendFile(self, filePath, chatId):
        media_id = self.getMedia_id(filePath)

        url = 'https://oapi.dingtalk.com/chat/send?access_token=' + self.access_token
        header = {
            'Content-Type': 'application/json'
        }
        data = {'access_token': self.access_token,
                'chatid': chatId,
                'msg': {
                    'msgtype': 'file',
                    'file': {'media_id': media_id}
                }}
        res = self.request.postJsonData(url=url, json=data, headers=header) #requests.request('POST', url, data=json.dumps(data), headers=header)
        if res['errcode'] == 0:
            print(filePath, '文件发送成功')
        else:
            print(filePath, '文件发送失败')


agentId = '1144185570'
appkey = 'dingb4zcg5o8ubkciavn'
appsecret = 'ff1dujPLmdGQAU19TJKKzxET96eIGHGzjny9XuxLNGh6LtSBRdfQZXuXWOdtNwTH'
chatId = 'chat7de921003c27badb1c9cc3b9d05ad7b8'
dt = DingTalk2(appkey, appsecret)
# res = dt.getMedia_id(filePath='/Users/xuxiang/Downloads/APScheduler.py')
# res = dt.SendFile(filePath='/Users/xuxiang/Downloads/APScheduler.py', chatId='chat7de921003c27badb1c9cc3b9d05ad7b8')
# res = dt.send_text_msg(chatId=chatId, content='测试测试')
res = dt.getChat(chatId)
print(res)