#!/usr/bin/python
# -*- coding: UTF-8 -*-
import hashlib
from urllib import urlencode
class DDser(object):

    def verify(self,params={},sign='',appkey=''):
        params = self.filter(params)
        linkString = self.createLinkString(params)
        sign = self.sign(linkString,appkey)
        return  sign

    def filter(self,params={}):
        ret={}
        for index in params:
            if index=='sign'or params[index]=='' or params[index].isspace():
                continue
            ret[index]=params[index]
        return ret
    def createLinkString(self,params={}):
        ret = self.http_build_query(params);
        return ret

    def http_build_query(self,params={}):
        params_2=sorted(params.iteritems(), key = lambda asd:asd[0],reverse=False)
        strurl=urlencode(params_2)

        return strurl
    def sign(self,linkString,appkey):
        sign = hashlib.md5()
        sign.update(linkString+'&'+appkey)
        # print "签名之前的url：",linkString+'&'+appkey
        sign=sign.hexdigest()
        return sign