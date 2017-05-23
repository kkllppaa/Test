# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
import json
import requests
import smtplib
from email.mime.text import MIMEText

def get_hitokoto():
    global resp1
    url1='http://api.lwl12.com/hitokoto/main/get'
    resp1=request.urlopen(url1).read().decode('utf-8')
    print(resp1)
    return resp1

def weather():
    global ganmao
    global f
    global f_list
    f_list=[]
    url2='http://wthrcdn.etouch.cn/weather_mini?citykey=101230101' #101230101,绂忓窞101230104,缃楁簮101230105,杩炴睙
    resp2=requests.get(url2).json()
    data=resp2.get('data')
    ganmao=data.get('ganmao')
    forecast=data.get('forecast')
    for fc in forecast:
        f=(fc.get('date'),fc.get('type'),fc.get('low'),fc.get('high'),fc.get('fengxiang'),fc.get('fengli'))
        f_list.append(f)            
    return f_list


def get_bing_photo():
    global img
    global img_alt
    url3='http://bing.plmeizi.com/'
    resp3=request.urlopen(url3)
    soup=BeautifulSoup(resp3,'html.parser')
    a=soup.find('a',class_="item")
    img=a.find('img').get('src')
    img_alt=a.find('img').get('alt')
    print(img_alt)
    return img,img_alt

#email信息
def email():
    global message
    message=MIMEText('''

    <font color="black">一言:</font><br>
    <font color="red">%s</font><br><br>
    <font color="black">一日:</font><br>
    <font color="red">%s</font><br>
    <font color="blue" size=“1”>%s</font><br>
    <font color="black" size=“1”>%s</font><br>
    <font color="black" size=“1”>%s</font><br>
    <font color="black" size=“1”>%s</font><br>
    <font color="black" size=“1”>%s</font><br><br>

    <font color="black">一图:</font><br>
    <img src="%s"><br>
    <font color="red">%s</font><br>

    '''%(resp1,ganmao,f_list[0],f_list[1],f_list[2],f_list[3],f_list[4],img,img_alt),'html','utf-8')

    message['Subject']='每日生活'
    message['From']=sender
    message['To']=receivers[0]


if __name__ == '__main__':
    #126服务器
    mail_host='smtp.126.com'

    #用户信息
    user_name='k200'
    user_password='52327628'
    sender='k200@126.com'
    receivers=['349611@qq.com']

    get_hitokoto()
    weather()
    get_bing_photo()
    email()
    #登入发送
    try:
        smtp=smtplib.SMTP(timeout=120)
        smtp.connect(mail_host,25)
        smtp.login(user_name,user_password)

        smtp.sendmail(sender,receivers,message.as_string())
        smtp.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('e')




