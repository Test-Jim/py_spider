#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from bs4 import  BeautifulSoup
import re,threading
import urllib2,os,time
class spider_bookbencom(object):
    def __init__(self):
        self.addr='http://www.bookben.com'
        # http://www.bookben.com/youxijingji/index_2.html
        # self.html=urllib2.urlopen(self.addr+'/youxijingji/')
        self.dirpath='D:\\spidernovels\\'

    def find_novels(self,url,flag):
        NNlist,downurl=[],[]
        html=urllib2.urlopen(self.addr+url)
        html.close
        # print "当前页面地址：",self.addr+url
        soup_1=BeautifulSoup(html,"html.parser")
        getNovel=soup_1.find_all('a',title=True,text=True,href=re.compile('shtml'),limit=20)
        for index in getNovel:
            try:
                NNlist.append(index.string)
                html=urllib2.urlopen(self.addr+index.get('href'))
                # soup=BeautifulSoup(html,"html.parser",from_encoding="gb18030")
                soup=BeautifulSoup(html,"html.parser",from_encoding="gbk")
                downloadurl=soup.find('a',href=re.compile(r'\.txt')).get('href').encode('utf-8')
                downurl.append(downloadurl)
            except:
                pass
        self.download(downurl,NNlist,flag)

    def makedir(self,dirpath):
        if os.path.exists(dirpath):
            return False
        else:
            print "创建 ",dirpath," 文件夹..."
            os.mkdir(dirpath)
            return True
    def download(self,down_url_ls,filename_ls,flag):
        for index in xrange(len(down_url_ls)):
            print "正在下载：",down_url_ls[index]
            data=urllib2.urlopen(down_url_ls[index]).read()
            if 'wangyou' in flag:
                filename=self.dirpath+u'网游\\'+filename_ls[index]+'.txt'
                with open(filename,'wb') as f:
                    f.write(data)
            if 'yanqing' in flag:
                filename=self.dirpath+u'言情\\'+filename_ls[index]+'.txt'
                with open(filename,'wb') as f:
                    f.write(data)
if __name__=='__main__':
    Threads=[]
    spider=spider_bookbencom()
    spider.makedir(spider.dirpath)
    Threads.append(threading.Thread(target=spider.find_novels,args=('/youxijingji/','wangyou',)))
    for index in xrange(2,21):
        Threads.append(threading.Thread(target=spider.find_novels,args=('/youxijingji/index_%s.html'%index,'wangyou',)))
    Threads.append(threading.Thread(target=spider.find_novels,args=('/yanqingxiaoshuo/','yanqing',)))   
    for index in xrange(2,6):
        Threads.append(threading.Thread(target=spider.find_novels,args=('/yanqingxiaoshuo/index_%s.html'%index,'yanqing',)))	
    for t in Threads:
        time.sleep(0.2)
        t.setDaemon(True)
        t.start()
    for t in Threads:
        time.sleep(0.2)
        t.join()

