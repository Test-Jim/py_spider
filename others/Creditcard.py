#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb,datetime,smtplib,xlwt
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
class CreditCards(object):
    def __init__(self):
        self.DBhost='10.11.104.228'
        self.DBport=3306
        self.DBuser='fastpay'
        self.DBpassword='Fastpay123456'
        self.DBname='fastpay'
        self.handle,self.conn=None,None
        self.curDate=datetime.date.today()
        self.oneday = datetime.timedelta(days=1)
    def connectDB(self):
        self.conn = MySQLdb.connect(host=self.DBhost, port=self.DBport, user=self.DBuser, passwd=self.DBpassword, db=self.DBname, charset='utf8')
        self.handle=self.conn.cursor()

    def sel_UserNum(self):
        #查询商户总数
        strsql="SELECT COUNT(*) FROM LC_FASTPAY_MERCHANT t WHERE t.MERCHANT_STATUS != 'REFUSED' AND CREATE_TIME <= '%s 17:30:00'"%self.curDate
        self.handle.execute(strsql)
        tup=self.handle.fetchall()
        return tup[0][0]
    def sel_UserChecked(self):
        #查询已审核商户数
        strsql="SELECT COUNT(*) FROM LC_FASTPAY_MERCHANT t WHERE t.MERCHANT_STATUS = 'SUCCESS' AND CREATE_TIME <= '%s 17:30:00'"%self.curDate
        self.handle.execute(strsql)
        tup=self.handle.fetchall()
        return tup[0][0]
    def sel_UserAdded(self):
        #查询新增商户数
        strsql="SELECT COUNT(*) from LC_FASTPAY_MERCHANT t WHERE t.MERCHANT_STATUS != 'REFUSED' AND t.CREATE_TIME > DATE_ADD(CURDATE(),INTERVAL -4 DAY)"
        self.handle.execute(strsql)
        tup=self.handle.fetchall()
        return tup[0][0]
    def sel_AmountAll(self):
        #查询已充值总金额
        strsql="SELECT SUM(t.ORDER_AMT) FROM LC_FASTPAY_ORDER_DETAIL t WHERE t.ORDER_STATE = '01' AND t.CREATE_TIME <= '%s 17:30:00'"%self.curDate
        self.handle.execute(strsql)
        tup=self.handle.fetchall()
        return tup[0][0]/100
    def sel_UserNew(self):
        #新增商户数
        strsql="SELECT count(*) from LC_FASTPAY_MERCHANT where MERCHANT_STATUS != 'REFUSED' and CREATE_TIME BETWEEN '%s 17:30:00' AND '%s 17:30:00'"%(self.curDate-self.oneday,self.curDate)
        self.handle.execute(strsql)
        tup=self.handle.fetchall()
        return tup[0][0]
    def sel_AmountNew(self):
        #新增充值金额
        strsql_1="select SUM(ORDER_AMT) from LC_FASTPAY_ORDER_DETAIL where ORDER_STATE='01'"
        strsql_2="select SUM(ORDER_AMT) from LC_FASTPAY_ORDER_DETAIL where ORDER_STATE='01' and CREATE_TIME <= '%s 17:30:00'"%(self.curDate-self.oneday)
        self.handle.execute(strsql_1)
        tup_1=self.handle.fetchall()
        self.handle.execute(strsql_2)
        tup_2=self.handle.fetchall()
        return (tup_1[0][0]-tup_2[0][0])/100
    def sel_Withdraw_cash(self):
        #已经使用提现通道的人员
        strsql="SELECT  o.CUSTOMER_NAME, o.PHONE_NO, SUM(o.ORDER_AMT) FROM LC_FASTPAY_ORDER_DETAIL o WHERE o.ORDER_STATE = '01' AND o.CREATE_TIME <= '%s 17:30:00' GROUP BY o.BIND_ID"%self.curDate
        self.handle.execute(strsql)
        tup = self.handle.fetchall()
        return tup

    def sel_Withoutdraw_cash(self):
        #未使用提现通道的人员
        strsql="SELECT m.ACCOUNT_NAME, m.MOBILE FROM LC_FASTPAY_MERCHANT m WHERE m.BIND_ID NOT IN (SELECT o.BIND_ID FROM LC_FASTPAY_ORDER_DETAIL o WHERE o.ORDER_STATE = '01' and o.CREATE_TIME <= '%s 17:30:00' GROUP BY o.BIND_ID ) AND m.MERCHANT_STATUS = 'SUCCESS' AND m.CREATE_TIME <= '%s 17:30:00'"%(self.curDate,self.curDate)
        self.handle.execute(strsql)
        tup=self.handle.fetchall()
        return tup
if __name__=='__main__':
    man=CreditCards()
    man.connectDB()
    UserNum=man.sel_UserNum()
    UserChecked=man.sel_UserChecked()
    UserAdded=man.sel_UserAdded()
    AmountAll=man.sel_AmountAll()
    UserNew=man.sel_UserNew()
    AmountNew=man.sel_AmountNew()
    Withdraw_cash=man.sel_Withdraw_cash()
    Withoutdraw_cash=man.sel_Withoutdraw_cash()

    def createExcel():
        excel=u'信用卡通道用户提现情况.xls'
        rb=xlwt.Workbook(encoding = 'utf-8')
        sheet1=rb.add_sheet(u'用户提现情况',cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'
        style.font = font
        row0=['提现序号','姓名','手机号','提现金额(元)','','未提现序号','姓名','手机号']
        for index in range(0,len(row0)):
            sheet1.write(0,index,row0[index],style)
        for index in xrange(1,len(Withdraw_cash)+1):
            sheet1.write(index,0,index)
            sheet1.write(index,1,Withdraw_cash[index-1][0])
            sheet1.write(index, 2, Withdraw_cash[index - 1][1])
            sheet1.write(index, 3, Withdraw_cash[index - 1][2]/100)
        for index in xrange(1,len(Withoutdraw_cash)+1):
            sheet1.write(index,5,index)
            sheet1.write(index,6,Withoutdraw_cash[index-1][0])
            sheet1.write(index, 7, Withoutdraw_cash[index - 1][1])
        rb.save(excel)


    createExcel()
    mail_host = "smtp.exmail.qq.com"  # 设置服务器
    mail_user = "hy@91licheng.cn"  # 用户名
    mail_pass = "Heyi123456"  # 口令
    sender = 'hy@91licheng.cn'
    # receivers = ['jzs@91licheng.cn']
    receivers = ['jzs@91licheng.cn','wangjl@91licheng.cn','cqiao@91licheng.cn','sxy@91licheng.cn','cheny@91licheng.cn']
    emailcontent = "各位领导：\n" \
                   "    商户总数（人）：%s\n" \
                   "    累计已审核商户数（人）：%s\n" \
                   "    累计充值金额（元）：%s\n" \
                   "    新增商户数（人）：%s\n" \
                   "    新增充值金额（元）：%s\n" \
                   "    累计已使用通道提现的商户数（人）：%s\n" \
                   "    累计未使用通道提现的商户数（人）：%s\n"%(UserNum,UserChecked,AmountAll,UserNew,AmountNew,len(Withdraw_cash),len(Withoutdraw_cash))
    message = MIMEMultipart()
    # message = MIMEText(emailcontent, 'plain', 'utf-8')
    message['From'] = Header("信用卡通道数据", 'utf-8')
    message['To'] = Header("各位领导", 'utf-8')
    # subject = '（%s）信用卡通道商户数据统计' % datetime.date.today()
    subject = '（%s 至 %s）信用卡通道商户数据统计'%(datetime.date.today()-datetime.timedelta(days=1),datetime.date.today())

    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(emailcontent, 'plain', 'utf-8'))

    att1 = MIMEText(open(u'信用卡通道用户提现情况.xls', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = "attachment; filename=%s信用卡通道用户提现情况.xls"%datetime.date.today()
    message.attach(att1)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"