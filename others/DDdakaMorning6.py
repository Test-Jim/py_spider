#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
PATH=lambda p:os.path.abspath(
os.path.join(os.path.dirname(__file__),p)
)
from appium  import webdriver
class dingding():
    def __init__(self):
        desired_caps={}
        desired_caps['device'] = 'android'
        desired_caps['platformName']='Android'#使用哪种移动平台
        #desired_caps['browserName']='Chrome'#移动浏览器名称
        desired_caps['version']='4.4.4'#安卓版本
        desired_caps['deviceName']='PLK-AL10'#这是测试机的型号，可以查看手机的关于本机选项获得
        # desired_caps['app'] = PATH('F:\\appiumjzs\dingding_456.apk')
        #如果知道被测试对象的apppage，appActivity可以加上下面这两个参数，如果不知道，可以注释掉，不影响用例执行
        desired_caps['appPackage']='com.alibaba.android.rimet' #待测试的app的java package
        desired_caps['appActivity']='com.alibaba.android.rimet.biz.SplashActivity' #待测试的app的Activity名字
        self.driver=webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
        self.driver.implicitly_wait(20)
    def test_login(self):
        time.sleep(10)
        #登录
        self.driver.find_element_by_id('com.alibaba.android.rimet:id/et_phone_input').clear().send_keys('15669036110')
        self.driver.find_element_by_id('com.alibaba.android.rimet:id/et_pwd_login').send_keys('qwertyuiop')
        self.driver.find_element_by_id('com.alibaba.android.rimet:id/btn_next').click()

        #切换到工作模块/找到考勤打卡功能/上班打卡
        self.driver.find_elements_by_id('com.alibaba.android.rimet:id/home_bottom_tab_icon')[1].click()
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'考勤打卡')]").click()
        time.sleep(5)
        self.driver.find_element_by_accessibility_id('上班打卡').click()
        time.sleep(1)
        self.driver.back()
        self.driver.find_elements_by_id('com.alibaba.android.rimet:id/home_bottom_tab_icon')[3].click()
        self.driver.swipe(520,1330,520,390,1000)
        time.sleep(1)
        self.driver.find_element_by_id('com.alibaba.android.rimet:id/rl_setting').click()
        self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'退出登录')]").click()
        time.sleep(2)
        self.driver.find_element_by_id('android:id/button1').click()



    def aaa(self):
        self.driver.quit()
        os.popen("adb wait-for-device")
        # packageName=['com.alibaba.android.rimet',"io.appium.unlock","io.appium.settings"]
        packageName=["io.appium.unlock","io.appium.settings"]
        for index in range(len(packageName)):
            os.popen("adb uninstall " + packageName[index])


DD=dingding()
DD.test_login()
# DD.aaa()
