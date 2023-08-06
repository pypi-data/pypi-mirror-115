'''
1、导入模块
2、使用yagmail的类创建对象（发件人，发件人授权码，发件服务器）
3、使用yagmail对象发送邮件（指定收件人，邮件主题，发送内容）
'''

#1、导入模块
import yagmail
import os

class SendEmail:
    # sender 发件人邮箱
    # password #邮箱授权码,通过在邮箱设置里面可查到
    # host 发件服务器 例如 smtp.qq.com
    def __init__(self, sender, password, host):
        self.ya_obj = yagmail.SMTP(user=sender, password=password, host=host)

    # receiver 收件人邮箱 'xxxxxxxx'，也可写成列表形式["xxxxxxxxx"]，收件人有多个则造成一个列表
    # subject 主题，
    # contents 内容
    # attachments 附件 #附件为列表形式，填入具体路径
    def send(self, receiver, subject=None, contents=None, attachments=None):
        try:
            self.ya_obj.send(to=receiver, subject=subject, contents=contents, attachments=attachments)
        except Exception as e:
            print('发送邮件出错:', e)


if __name__ == "__main__":
    se = SendEmail(sender='1456127594@qq.com', password='wfnnyzdkgbwpfjjc', host='smtp.qq.com')

    # 发送无主题无内容无附件邮件
    se.send('xu_xiang_1@163.com')

    # 发送有主题无内容无附件邮件
    se.send('xu_xiang_1@163.com', subject='有主题无内容无附件邮件')

    # 发送无主题有内容无附件的邮件
    se.send('xu_xiang_1@163.com', contents='无主题有内容无附件')

    # 发送有主题有内容无附件的邮件
    se.send('xu_xiang_1@163.com', subject='有主题有内容无附件', contents='测试一下')

    # 发送有主题有内容有附件的邮件
    se.send('xu_xiang_1@163.com',subject='有主题有内容有附件的邮件', contents='测试一下', attachments=r'/Users/xuxiang/Pictures/5302d3ac48b09.jpg')

    # 发送有图片内容的邮件
    se.send('xu_xiang_1@163.com', subject='有图片内容的邮件', contents=['测试一下',yagmail.inline(r'/Users/xuxiang/Pictures/5302d3ac48b09.jpg')])

