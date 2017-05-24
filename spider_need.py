#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re
import connetmysql
from bs4 import BeautifulSoup
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
data={'account':'jinzhangshuang','password':'26273b5e9eab8fd735c7ef8f47fce034','keepLogin[]':'on',
      'rederer':'http://project.kuaiqiangche.cc/index.php?m=company&f=browse'}

def all():
    s=requests.session()

    loginUrl='http://project.kuaiqiangche.cc/index.php?m=user&f=login'
    # allUrl=['http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id=52',
    #         'http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id=53',
    #         'http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id=55',
    #         'http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id=57',
    #         'http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id=56',
    #         'http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id=58',
    #         'http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id=54']

    login=s.post(url=loginUrl,data=data,headers=headers)
    for index in range(52,100):
        try:
            url='http://project.kuaiqiangche.cc/index.php?m=productplan&f=view&id='+str(index)
            response=s.get(url=url,cookies = login.cookies,headers=headers)

            soup=BeautifulSoup(response.content,'lxml')
            responselist_1=soup.find_all("a", href=re.compile("storyID"),text=True)
            responselist_2=soup.find_all("td",class_=re.compile("story-"),text=True)
            responselist_3=re.findall(re.compile(r'宝(.*?)上线'),str(soup.title.string))

            need_id,need_name,need_status,need_url=[],[],[],[]
            for index in range(len(responselist_1)):
                    if index%2==0:
                        need_id.append(responselist_1[index].string)
                        need_url.append("http://project.kuaiqiangche.cc"+responselist_1[index].attrs['href'])
                    else:
                        need_name.append(responselist_1[index].string)
                        need_status.append(responselist_2[index/2].string)
            print need_id
            # for index in range(len(responselist_1)):
            #     print need_id[index],need_name[index],need_status[index],need_url[index]
            handle,conn=connetmysql.Mysql.connet()
            connetmysql.Mysql.insert_need(handle,need_id,need_name,need_status,need_day=responselist_3[0],need_url=need_url)
            connetmysql.Mysql.close(handle,conn)
        except Exception,e:
            pass

a=all()