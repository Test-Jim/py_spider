#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib,datetime
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "hy@91licheng.cn"  # 用户名
mail_pass = "Heyi123456"  # 口令

sender = 'hy@91licheng.cn'
receivers = ['jzs@91licheng.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
emailcontent=''
message = MIMEText(emailcontent, 'plain', 'utf-8')
message['From'] = Header("信用卡通道数据", 'utf-8')
message['To'] = Header("各位领导", 'utf-8')

subject = '（%s）信用卡通道商户数据统计'%datetime.date.today()
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "邮件发送成功"
except smtplib.SMTPException:
    print "Error: 无法发送邮件"