#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
class CreditCards(object):
    def __init__(self):
        self.DBhost='115.238.64.146'
        self.DBport=6150
        self.DBuser='root'
        self.DBpassword='root'
        self.DBname_1='coupon_test'
        self.handle,self.conn=None,None
        self.companyid=137
    def connectDB(self):
        self.conn = MySQLdb.connect(host=self.DBhost, port=self.DBport, user=self.DBuser, passwd=self.DBpassword, db=self.DBname_1, charset='utf8')
        self.handle=self.conn.cursor()
    def getCompanyMoney(self):
        #获取企业和平台的可用余额、冻结金额、总金额
        strsql="select BALANCE_MONEY,FROZEN_MONEY,ACCOUNT_TOTAL_MOENY from COUPON_ACCOUNT_BUSINESS where COMPANY_ID=%s;"%self.companyid
        self.handle.execute(strsql)
        tup=self.handle.fetchall()
        return tup[0]
    def getMoneyRecord(self):
        #获取企业和平台的操作记录
        strsql="SELECT a.BUSINESS_TYPE_DESC,a.MONEY,a.CREATE_TIME  from  " \
               "COUPON_ACCOUNT_REQUEST as a INNER JOIN COUPON_ACCOUNT_BUSINESS as b on a.ACCOUNT_NO=b.ACCOUNT_NO where b.COMPANY_ID=%s ORDER BY a.CREATE_TIME desc;" %self.companyid
        self.handle.execute(strsql)
        tup = self.handle.fetchall()
        return tup[0]
if __name__=='__main__':
    jzs=CreditCards()
    jzs.connectDB()
    money=jzs.getCompanyMoney()
    print 'BALANCE_MONEY：',money[0],'   FROZEN_MONEY：',money[1],'   ACCOUNT_TOTAL_MOENY',money[2],'  算出总金额：',money[0]+money[1]
    order=jzs.getMoneyRecord()
    print '动作：',order[0],'   金额：',order[1]
    money=jzs.getCompanyMoney()
    print '动作执行之后BALANCE_MONEY：',money[0],'动作执行之后FROZEN_MONEY：',money[1],'动作执行之后ACCOUNT_TOTAL_MOENY',money[2],'动作执行之后算出总金额：',money[0]+money[1]
