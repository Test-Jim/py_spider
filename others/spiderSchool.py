#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2,re,xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class spider_School(object):
    def __init__(self):
        self.url='http://www.ruyile.com/xuexiao/?a=%s&t=4&p=%s'

    def begin(self):
        enlist = []
        html = urllib2.urlopen(self.url%1)
        soup=BeautifulSoup(html,"html.parser")

        num = soup.find_all('span', class_='zys')
        school=soup.find_all('div',class_='sk')

        for index in school:
            alist=re.split(u'[：|地址]',index.text)
            enlist.append(alist)
        for page in xrange(2, int(num[0].string) + 1):
            html = urllib2.urlopen(self.url%page)
            soup = BeautifulSoup(html, "html.parser")
            school = soup.find_all('div', class_='sk')
            for index in school:
                alist=re.split(u'[：|地址]',index.text)
                enlist.append(alist)
        for ii in enlist:
            while '' in ii:
                ii.remove('')
        return  enlist

    def excel(self,enlist):
        # 把数据保存到excel里
        excel = u'专科高职表.xls'
        rb = xlwt.Workbook(encoding='utf-8')
        sheet1 = rb.add_sheet(u'浙江省专科高职表', cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'
        style.font = font
        row0 = ['校名', '电话', '地址/电话/邮编', '地址/邮编','地址']
        for index in range(0, len(row0)):
            sheet1.write(0, index, row0[index], style)
        for index in xrange(len(enlist)):
            try:
                sheet1.write(index + 1, 0, enlist[index][0].replace('电话',''))
                sheet1.write(index + 1, 1, enlist[index][1].replace('传真','').replace('传    真','').replace('邮编',''))
                sheet1.write(index + 1, 2, enlist[index][2].replace('邮编',''))
                sheet1.write(index + 1, 3, enlist[index][3])
                sheet1.write(index + 1, 4, enlist[index][4])
            except :
                continue
        rb.save(excel)

jzs=spider_School()
enlist=jzs.begin()
jzs.excel(enlist)
