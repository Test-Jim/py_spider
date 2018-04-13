#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb,datetime,smtplib,xlwt
import MySQLdb.cursors
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import datetime as da
endday= da.date.today()-da.timedelta(days=1)
# endday=da.date.today()
class Userdata(object):
    def __init__(self):
        self.DBhost='10.11.104.228'
        self.DBport=3306
        self.DBuser='jzs'
        self.DBpassword='123456'
        self.DBname='USER'
        self.DBname2= 'ORDER'
        self.DBname3='CMS'
        self.DBname4 = 'COUPON'
        # self.curDate=datetime.date.today()
        # self.oneday = datetime.timedelta(days=1)
        # self.endday= da.date.today()-da.timedelta(days=1)
    def connectDB(self):
        self.conn = MySQLdb.connect(host=self.DBhost, port=self.DBport, user=self.DBuser, passwd=self.DBpassword, db=self.DBname, charset='utf8',cursorclass=MySQLdb.cursors.DictCursor)
        self.handle_user=self.conn.cursor()
        self.conn=MySQLdb.connect(host=self.DBhost, port=self.DBport, user=self.DBuser, passwd=self.DBpassword, db=self.DBname2, charset='utf8')
        self.handle_order = self.conn.cursor()
        self.conn=MySQLdb.connect(host=self.DBhost, port=self.DBport, user=self.DBuser, passwd=self.DBpassword, db=self.DBname3, charset='utf8')
        self.handle_cms = self.conn.cursor()
        self.conn=MySQLdb.connect(host=self.DBhost, port=self.DBport, user=self.DBuser, passwd=self.DBpassword, db=self.DBname4, charset='utf8')
        self.handle_coupon = self.conn.cursor()
    def closeDB(self):
        self.conn.close()
        self.handle_cms.close()
        self.handle_order.close()
        self.handle_user.close()
        self.handle_coupon.close()

    def sel_product(self):
        #查询标的名称
        strsql="select id ,name from CMS_ASSET_PACKAGE"
        self.handle_cms.execute(strsql)
        tup=self.handle_cms.fetchall()
        user_dict={}
        for index in tup:
            user_dict[index[0]]=index[1]
        return  user_dict

    def sel_user(self):
        #查询商户总数
        strsql="select a.mobile,c.REAL_NAME,b.REAL_ID from LQB_USER as a INNER JOIN LC_USER_PLATFORM as b INNER JOIN LC_REAL_USER as c on a.ID=b.USER_ID and b.REAL_ID=c.ID"
        self.handle_user.execute(strsql)
        tup=self.handle_user.fetchall()
        return tup

    def sel_orderinfo(self):
        #查询购买数据
        strsql="select PRODUCT_ID,MONEY , TOTAL_RED_ENVELOPE_MONEY , TOTAL_MONEY ,RETURNED_MONEY_STATE_DESC ,BUSINESS_STATUS_DESC,USER_ID, PAY_TYPE_DESC, CREATE_TIME " \
               "from ORDER_INFO where CREATE_TIME like'%s%%' ORDER BY CREATE_TIME"%endday
        self.handle_order.execute(strsql)
        tup=self.handle_order.fetchall()
        return list(tup)

    def sel_company_yue(self):
        #查询企业余额
        strsql="select BALANCE_MONEY,FROZEN_MONEY,ACCOUNT_TOTAL_MOENY from COUPON_ACCOUNT_BUSINESS where id =9"
        self.handle_coupon.execute(strsql)
        tup=self.handle_coupon.fetchall()
        return tup

    def mobile_user(self,tup):
        #重新生成real_id:[user,mobile]字典
        self.re_dict = {}
        for index in tup:
            if index['REAL_NAME']=='':
                continue
            else:
                self.re_dict[index['REAL_ID']]=[index['mobile'],index['REAL_NAME']]
        return self.re_dict

    def createExcel(self,list_order,company_yue):
        #把数据保存到excel里
        excel = '%sUserOrderData.xls'%endday
        rb = xlwt.Workbook(encoding='utf-8')
        sheet1 = rb.add_sheet(u'用户下单情况', cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'
        style.font = font
        row0 = ['标的', '实际投资金额', '使用红包金额', '总金额', '回款情况', '下单情况', '姓名','手机号', '时间','余额','冻结金额','总金额']
        for index in range(0, len(row0)):
            sheet1.write(0, index, row0[index], style)
        for index in xrange(len(list_order)):
            sheet1.write(index+1, 0, list_order[index][0])
            sheet1.write(index+1, 1, list_order[index][1])
            sheet1.write(index+1, 2, list_order[index][2])
            sheet1.write(index+1, 3, list_order[index][3])
            sheet1.write(index+1, 4, list_order[index][4])
            sheet1.write(index+1, 5, list_order[index][5])
            sheet1.write(index+1, 6, list_order[index][6])
            sheet1.write(index+1, 7, list_order[index][7])
            sheet1.write(index+1, 8, list_order[index][8].strftime("%Y-%m-%d %H:%M:%S"))
        sheet1.write(1,9,company_yue[0][0])
        sheet1.write(1,10, company_yue[0][1])
        sheet1.write(1,11, company_yue[0][2])
        rb.save(excel)

if __name__=='__main__':
    jzs=Userdata()
    jzs.connectDB()
    tup=jzs.sel_user()
    #查询用户信息
    dict=jzs.mobile_user(tup)
    company_yue=jzs.sel_company_yue()
    #做出第一个excel表
    def first_excel():
        list_order=jzs.sel_orderinfo()
        list_order=[list(item) for item in list_order]
        product_dict=jzs.sel_product()
        for index in range(len(list_order)):
            ruUser=list_order[index][6]
            productid=list_order[index][0]
            if ruUser in dict:
                list_order[index][6]=dict[ruUser][1]
                list_order[index][7] = dict[ruUser][0]
            if product_dict[int(productid)]:
                list_order[index][0]=product_dict[int(productid)]
        jzs.createExcel(list_order,company_yue)
    first_excel()
    jzs.closeDB()
    def sendEmail():
        mail_host = "smtp.exmail.qq.com"  # 设置服务器
        mail_user = "st@91licheng.cn"  # 用户名
        mail_pass = "SHItian520"  # 口令
        sender = 'st@91licheng.cn'
        # receivers = ['CHrosyealighting@outlook.com']
        receivers = ['CHrosyealighting@outlook.com','511390568@qq.com']
        emailcontent = "前一天附件"
        message = MIMEMultipart()
        # message = MIMEText(emailcontent, 'plain', 'utf-8')
        message['From'] = Header("商户端需要的数据", 'utf-8')
        message['To'] = Header("博时轩财务", 'utf-8')
        # subject = '（%s）信用卡通道商户数据统计' % datetime.date.today()
        subject = '博时轩需要的数据'

        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(emailcontent, 'plain', 'utf-8'))

        att1 = MIMEText(open('%sUserOrderData.xls'%endday, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = "attachment; filename=%sUserOrderData.xls" % endday
        message.attach(att1)
        try:
            # smtpObj = smtplib.SMTP()
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            # smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print "邮件发送成功"
        except smtplib.SMTPException:
            print "Error: 无法发送邮件"

    import time
    time.sleep(1)
    sendEmail()