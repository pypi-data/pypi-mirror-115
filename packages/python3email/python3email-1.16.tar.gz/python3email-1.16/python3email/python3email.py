# @Time:2021/8/5 11:11
# @Software: PyCharm
# Author: maisge
#QQ2696047693
# !/usr/bin/python3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def login(host,port,user,password):
    global s
    global user_
    user_=user



    s=smtplib.SMTP_SSL(host,port)


    temp=s.login(user,password)

    try:
        if temp[1]=="Authentication successful":
            return ["邮箱登录成功","login ok"]
    except Exception as e:
        return e

def send(to,dict):
    message = MIMEText(str(dict["text"]), 'plain', 'utf-8')
    message['From'] = Header(str(dict["mytitle"]), 'utf-8')  # mytitle
    message['To'] = Header(str(dict["totitle"]), 'utf-8')  # totitle

    a = s.sendmail(user_, to, message.as_string())
    print("邮件发送成功")




#login("smtp.qq.com",465,"2696047693@qq.com","xvtclnqsuitgdgbj")
#dict={"text":666,"mytitle":7777,"totitle":66}
#send("2696047693@qq.com",dict)

