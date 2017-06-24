#!/usr/bin/env python
# coding:utf-8
import smtplib
from email.mime.text import MIMEText


mail_host = 'smtp.163.com'
mail_user = 'atlantissgc'
mail_pass = 'guo233234'
mail_postfix = '163.com'


def send_mail(to_list, subject, content):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == "__main__":
    send_mail('506226866@qq.com', 'Atlantis 账号激活', '请确认账号信息')
