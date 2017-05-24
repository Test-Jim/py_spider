#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb,sys
import  requests,datetime,time
import DDservice
reload(sys)
sys.setdefaultencoding('utf-8')

class DDsend():
    def __init__(self):
        #链接线上数据库
        self.conn=MySQLdb.connect(host='121.42.173.230',port=3306,user='kqctest',passwd='test111',db='kqc_2016',charset='utf8')
        self.handle=self.conn.cursor()
        self.sess=requests.session()
        self.appid='kqc58c0f6188099aRxDK'
        self.appkey='93sqmDhnJiFch6QC2cYG6k3Yv12Nk8EL'
        self.nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.nowtime_2=time.time()
    def getphone(self):
        #获取当前公司人员所有的手机号
        sql_str="select phone from erp_admin_acount "
        self.handle.execute(sql_str)
        tup=self.handle.fetchall()
        phone=[]
        for index in tup:
            phone.append(index[0])
        phone.remove('18916575888')
        return ','.join(phone)

    def get_carSource(self,phone):
        #查询出公司人员的车源线上数据
        sql_str="SELECT a.type_title,b.name from" \
                " b2b_car_source as a INNER JOIN b2b_user as b  WHERE b.mobile in (%s) " \
                "and a.deleted_at =0 and a.user_id=b.id and a.status=1 and a.test_type=0 order by b.name"%str(phone)
        self.handle.execute(sql_str)
        tup=self.handle.fetchall()
        return tup

    def get_carFind(self,phone):
        #查出公司人员的寻车线上数据
        sql_str="SELECT a.fc_no,b.name from " \
                "b2b_find_car as a INNER JOIN b2b_user as b where a.user_id=b.id and a.status in (5,15)" \
                " and a.deleted_at =0 and b.mobile in (%s) and a.test_type=0 order by b.name"%str(phone)
        self.handle.execute(sql_str)
        tup=self.handle.fetchall()
        return tup

    def dd_tuisong_source(self,info):
        #发送钉钉推送给别人
        if info!= {}:
            for key in info.iteritems():
                # data_inside='{"msgtype":"text","message":"您当前线上在售车源有%s辆:%s,如要删除或者确认，请点击下方链接。当前时间：%s","names":"%s"}'\
                #             %(len(key[1]),str(key[1]).replace('u\'','\'').replace(',',',\n').decode("unicode-escape").encode('utf8'),str(time.time()),"金张爽")
                data_inside='{"msgtype":"text","message":"%s,您当前线上在售车源有%s辆,可能是测试数据,如要删除或者确认，请点击下方链接http://admin.kuaiqiangche.com/B2BCarFilter/carSourceList当前时间：%s","names":"%s"}'\
                            %(str(key[0]),len(key[1]),str(self.nowtime),str(key[0]))
                print data_inside
                params={'appid':self.appid,'data':data_inside,'source':'App\jzs\ddsend::f','type':'dingding'}
                instan=DDservice.DDser()
                sign=instan.verify(params=params,appkey=self.appkey)
                data={'appid':self.appid,'data':data_inside,'source':'App\jzs\ddsend::f','type':'dingding','sign':sign}
                response=self.sess.post(url='http://service.kuaiqiangche.cc/push?',data=data)
                print '返回：',response.text
                time.sleep(1)
    def dd_tuisong_find(self,info):
            #发送钉钉推送给别人
        if info!= {}:
            for key in info.iteritems():
                data_inside='{"msgtype":"text","message":"您当前线上寻车数据有%s条,可能是测试数据，如要删除或者确认，请点击下方链接http://admin.kuaiqiangche.com/B2BCarFilter/findCarList当前时间：%s","names":"%s"}'\
                            %(len(key[1]),str(self.nowtime),str(key[0]))
                params={'appid':self.appid,'data':data_inside,'source':'App\jzs\ddsend::f','type':'dingding'}
                instan=DDservice.DDser()
                sign=instan.verify(params=params,appkey=self.appkey)
                data={'appid':self.appid,'data':data_inside,'source':'App\jzs\ddsend::f','type':'dingding','sign':sign}
                response=self.sess.post(url='http://service.kuaiqiangche.cc/push?',data=data)
                print '返回：',response.text
                time.sleep(1)

    def dd_tuisong_self(self,info,summun):
        if info!= {}:
            #发送钉钉推送给自己
            #data_inside='{"msgtype":"text","message"：%s 当前时间：%s,"names":"%s"}'\
            #%(str(info).replace('u\'','\'').decode("unicode-escape").encode('utf8'),str(time.time()),"金张爽")
            data_inside='{"msgtype":"text","message":"您当前线上车源或者寻车数据%d条，可能是测试数据，如要删除或者确认，请点击下方链接。当前时间:%s","names":"%s"}'%(summun,str(self.nowtime),"金张爽")
            params={'appid':self.appid,'data':data_inside,'source':'App\jzs\ddsend::f','type':'dingding'}
            instan=DDservice.DDser()
            sign=instan.verify(params=params,appkey=self.appkey)
            data={'appid':self.appid,'data':data_inside,'source':'App\jzs\ddsend::f','type':'dingding','sign':sign}
            response=self.sess.post(url='http://service.kuaiqiangche.cc/push?',data=data)
            print '返回2：',response.text
            time.sleep(1)
    def db_close(self):
        self.handle.close()
        self.conn.close()
if __name__=='__main__':
    info,info2,sumnum={},{},0
    dd=DDsend()
    phone=dd.getphone()
    tup_source=dd.get_carSource(phone)
    tup_find=dd.get_carFind(phone)
    for value,key in tup_source:
        info.setdefault(key,[]).append(value)
    # for key in info.iteritems():
    #     print key[0]
    dd.dd_tuisong_source(info)
    # for key in info.iteritems():
    #     sumnum+=len(key[1])
    # dd.dd_tuisong_self(info,sumnum)


    # for value,key in tup_find:
    #     info2.setdefault(key,[]).append(value)
    # dd.dd_tuisong_find(info2)
    # for key in info2.iteritems():
    #     sumnum+=len(key[1])
    # dd.dd_tuisong_self(info2,sumnum)

    dd.db_close()