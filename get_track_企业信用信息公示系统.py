# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:10:16 2017

@author: liuxinyu
"""

#-*-coding:utf-8-*-
import requests
import re
from functools import reduce
from io import BytesIO as StringIO
from PIL import Image
#import random
#import math
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup
from random import randint
import numpy as np
import process_sample_track as pst
import pandas as pd
class crack_picture(object):
    def __init__(self, img_url1, img_url2):
        self.img1, self.img2 = self.picture_get(img_url1, img_url2)


    def picture_get(self, img_url1, img_url2):
        hd = {"Host": "static.geetest.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        img1 = StringIO(self.repeat(img_url1, hd).content)
        img2 = StringIO(self.repeat(img_url2, hd).content)
        return img1, img2


    def repeat(self, url, hd):
        times = 10
        while times > 0:
            try:
                ans = requests.get(url, headers=hd)
                return ans
            except:
                times -= 1   


    def pictures_recover(self):
        xpos = self.judge(self.picture_recover(self.img1, 'img1.jpg'), self.picture_recover(self.img2, 'img2.jpg')) - 6
        return self.darbra_track(xpos)


    def picture_recover(self, img, name):
        a =[39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        im = Image.open(img)
        im_new = Image.new("RGB", (260, 116))
        for row in range(2):
            for column in range(26):
                right = a[row*26+column] % 26 * 12 + 1
                down = 58 if a[row*26+column] > 25 else 0
                for w in range(10):
                    for h in range(58):
                        ht = 58 * row + h
                        wd = 10 * column + w
                        im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))
        im_new.save(name)
        return im_new


    def darbra_track(self, distance):
        return [[distance, 0.5, 1]]
        #crucial trace code was deleted


    def diff(self, img1, img2, wd, ht):
        rgb1 = img1.getpixel((wd, ht))
        rgb2 = img2.getpixel((wd, ht))
        tmp = reduce(lambda x,y: x+y, map(lambda x: abs(x[0]-x[1]), zip(rgb1, rgb2)))
        return True if tmp >= 200 else False

            
    def col(self, img1, img2, cl):
        for i in range(img2.size[1]):
            if self.diff(img1, img2, cl, i):
                return True
        return False


    def judge(self, img1, img2):
        for i in range(img2.size[0]):
            if self.col(img1, img2, i):
                return i
        return -1


class gsxt(object):
    def __init__(self, br_name="phantomjs"):
        self.br = self.get_webdriver(br_name)
        self.wait = WebDriverWait(self.br, 10, 1.0)
        self.br.set_page_load_timeout(20)
        self.br.set_script_timeout(20)


    def input_params(self, name):
        self.br.get("http://www.gsxt.gov.cn/index")
        element = self.wait_for(By.ID, "keyword")
        element.send_keys(name)
        time.sleep(1.1)
        element = self.wait_for(By.ID, "btn_query")
        element.click()
        time.sleep(1.1)


    def drag_pic(self):
        return (self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_fullbg_slice")),
               self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_bg_slice")))
        
    
    def wait_for(self, by1, by2):
        return self.wait.until(EC.presence_of_element_located((by1, by2)))


    def find_img_url(self, element):
        try:
            return re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
        except:
            return re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")
        
        

#    def get_random_track(L):
#    #            L = 100 # 这两个值任意更改，也可以用sys.argv来设置
#            n = 20
#            lst = []
#            j = L 
#            k = L 
#            for i in range(n-1): # 随机生成前面n-1个数
#                while j > ( k - (n - i) ): # 防止随机数太大，让后面的数不够分
#                    j = randint(-3, k)
#                lst.append( j ) 
#                k -= j
#                j = k        
#            lst.append( L - sum(lst) ) # 最后一个数字，用减法        
#            print( lst, sum(lst))
#            return lst
#        
#    def get_random_track2(self,L):
##        base_x=list(range(1,L))
#        base_x=list(np.ones(L,dtype=int))
#        return base_x


    def emulate_track(self, tracks):
        element = self.br.find_element_by_class_name("gt_slider_knob")
        x=tracks[0][0]
        print(x)
        rootdir = "f:\geetest"
        data_df=pst.get_track(rootdir)
        x_series=pd.to_numeric(data_df[0])
        y_series=pd.to_numeric(data_df[1])
        t_series=pd.to_numeric(data_df[2])
        x_lst=pst.process_series(x_series,length=x-2)
        y_lst=pst.process_y(y_series)
        new_t_lst=pst.process_time(t_series)
        new_t_lst_2=[]
        for timepoint in new_t_lst:
            new_t_lst_2.append(timepoint*0.001)
        #按下滑动块
        ActionChains(self.br).click_and_hold(on_element=element).perform()        
        time.sleep(0.3)
        
        for i in range(0,len(x_lst)):
            ActionChains(self.br).move_to_element_with_offset(
                    to_element=element, 
                    xoffset=x_lst[i]+22,
                    yoffset=y_lst[i]).perform()
            time.sleep(new_t_lst_2[i])
        

#        time.sleep(0.05)
        time.sleep(0.05)
        ActionChains(self.br).release(on_element=element).perform()
        time.sleep(0.8)
        element = self.wait_for(By.CLASS_NAME, "gt_info_text")
        ans = element.text
#        print(ans)
        return ans


    def run(self):
        
        for i in [u'招商银行']:            
        	   self.hack_geetest(i)
        	   time.sleep(1)
#        try:
#            for i in [u'招商银行']:            
#            	   self.hack_geetest(i)
#            	   time.sleep(1)
#        except:
#            self.quit_webdriver()
        


    def hack_geetest(self, company=u"招商银行"):
        flag = True
        self.input_params(company)
        while flag:
            img_url1, img_url2 = self.drag_pic()
            tracks = crack_picture(img_url1, img_url2).pictures_recover()
            tsb = self.emulate_track(tracks)
#            print(tsb)
            if '通过' in tsb:
                print('通过')
                print(tsb)
                time.sleep(1)
                print('find content')
                soup = BeautifulSoup(self.br.page_source, 'html.parser')
                for sp in soup.find_all("a", attrs={"class":"search_list_item"}):
                    print(re.sub(r"\s+", r"", sp.get_text().encode("utf-8")))
#                     输出页面内容
                    print (sp.get_text())
                break
            
            elif '吃' in tsb:
                print('失败')
                time.sleep(5)
            else:
                self.input_params(company)
                              

    def quit_webdriver(self):
        self.br.quit()


    def get_webdriver(self, name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
            return webdriver.PhantomJS(executable_path='E:/Anaconda3/selenium/webdriver/phantomjs-2.1.1-windows/bin/phantomjs.exe',desired_capabilities=dcap)

        elif name.lower() == "chrome":
            return webdriver.Chrome()


if __name__ == "__main__":
    gsxt("chrome").run()
    #print crack_picture("http://static.geetest.com/pictures/gt/fc064fc73/fc064fc73.jpg", "http://static.geetest.com/pictures/gt/fc064fc73/bg/7ca363b09.jpg").pictures_recover()
#    for i in range(1,10):
#        print('第'+str(i)+'次')
#        try:
#            gsxt("chrome").run()
#        except:
#            print('exception')
#            continue

#    for i in range(1,2):
#        print('第'+str(i)+'次')
#        try:
#            gsxt("chrome").run()
#        except:
#            print('exception')
#            continue

