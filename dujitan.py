#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import requests,json,random
from bs4 import BeautifulSoup
import urllib2,datetime
import sys,re
reload(sys)
sys.setdefaultencoding('utf8')
def spider_dujitang():
    conn=MySQLdb.connect(host='114.215.30.0',port=3306,user='root',passwd='admin',db='testjzs',charset='utf8')
    handle=conn.cursor()
    jtlist=[]
    html=urllib2.urlopen('http://www.yuwenmi.com/lizhi/qingchun/289706.html')
    soup=BeautifulSoup(html,"html.parser")
    plist=soup.find_all('p',class_=False,style=False)
    # plist.remove(None)
    for index in plist[1:]:
        try:
            jtlist.append(index.string.split('、',1)[1])
        except:
            pass
    for index in xrange(len(jtlist)-1):
        strsql="insert into dujitang (name) values ('%s')"%(jtlist[index+1])
        handle.execute(strsql)
    handle.close()
    conn.close()

def robot():
    conn=MySQLdb.connect(host='114.215.30.0',port=3306,user='root',passwd='admin',db='testjzs',charset='utf8')
    handle=conn.cursor()
    strsql="select name from dujitang where id=%d"%random.randint(1,98)
    handle.execute(strsql)
    tup=handle.fetchall()

    s=requests.session()
    data={"msgtype":"text",
          "text":{"content":"每日一碗鸡汤:%s,"%tup[0][0]},
          "at": {"isAtAll": False}}
    data=json.dumps(data)
    url='https://oapi.dingtalk.com/robot/send?access_token=d4d55624533ce572781d6a6fc38bf313f4c027173a0b813b9fb82577a5cc39e0'
    s.post(url=url,data=data,headers={'Content-Type': 'application/json'})

    handle.close()
    conn.close()

def history_today():
    s=requests.Session()
    mouth=datetime.datetime.now().strftime('%m')
    day=datetime.datetime.now().strftime('%d')
    url='http://api.juheapi.com/japi/toh?key=d47bc2a2fd27ea77946a34145acad985&v=2.0&month=%d&day=%d'%(int(mouth),int(day))
    response=s.get(url=url)
    end=response.json()
    connetstr=''
    for index in xrange(len(end['result'])):
        connetstr=connetstr+end['result'][index]['des']+'\n'
    print connetstr
    data={"msgtype":"text",
          "text":{"content":"历史上的今天:\n%s"%connetstr},
          "at": {"isAtAll": False}}
    data=json.dumps(data)
    url='https://oapi.dingtalk.com/robot/send?access_token=d4d55624533ce572781d6a6fc38bf313f4c027173a0b813b9fb82577a5cc39e0'
    s.post(url=url,data=data,headers={'Content-Type': 'application/json'})

def Ancient_poetry(flag=None):
    conn=MySQLdb.connect(host='114.215.30.0',port=3306,user='root',passwd='admin',db='testjzs',charset='utf8')
    handle=conn.cursor()
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    if flag ==None:
        req=urllib2.Request('http://www.360doc.com/content/11/0828/09/7198992_143832365.shtml',headers=headers)
        html=urllib2.urlopen(req).read()
        soup=BeautifulSoup(html,"html.parser")
        content=soup.find_all('span',style=re.compile('FONT-SIZE'),text=True)
        for index in content:
            print index.text[4:].split('－')[0]
            handle.execute("insert into poetry (content,title) VALUES ('%s','%s')"%(index.text[4:].split('－')[0],index.text[4:].split('－')[1]))

    else:
        strsql="select title,content from poetry where id=%d"%random.randint(1170,1268)
        handle.execute(strsql)
        tup=handle.fetchall()
        s=requests.session()
        data={"msgtype":"text",
              "text":{"content":"每日一句情诗:\n%s\n\n                         --%s"%(tup[0][1],tup[0][0])},
              "at": {"isAtAll": False}}
        data=json.dumps(data)
        url='https://oapi.dingtalk.com/robot/send?access_token=d4d55624533ce572781d6a6fc38bf313f4c027173a0b813b9fb82577a5cc39e0'
        s.post(url=url,data=data,headers={'Content-Type': 'application/json'})
    handle.close()
    conn.close()




a=Ancient_poetry(flag=True)