# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 09:42:10 2017

@author: liuxinyu
"""
#%%
import os
import os.path
import csv
from pandas import DataFrame
import pandas as pd
#import numpy as np
#import random
#%% 



def process_series(series,length=0):
    #全部减去起始点像素, 得到滑动轨迹
    base=series-series.iloc[0]
    #全部除以终点像素, 得到滑动的比例
    rate=base/base.iloc[-1]
    new_track=length*rate
    new_list=[]
    for x in new_track:
        new_list.append(int(x))
    
    new_new_x_series=[]
    for i in range(len(new_list)-1):
        new_new_x_series.append(new_list[i+1]-new_list[i])
    new_new_x_df=pd.Series(new_new_x_series)
    return new_new_x_df    


def process_y(y_series):
    y_series=y_series-y_series.iloc[0]
    new_new_y_series=[]
    for i in range(len(y_series)-1):
        new_new_y_series.append(y_series[i+1]-y_series[i])
    return new_new_y_series
#%%处理时间
def process_time(t_series):
    t_base=t_series-t_series.iloc[0]
    t_processed=[]
    for i in range(len(t_base)-1):
        t_processed.append((t_base[i+1]-t_base[i])/1000)
    return t_processed
        
#%%
def get_track(rootdir):
    
    file_list=[]
    for root,dirs,files in os.walk(rootdir):
        for file in files:
            filepath=rootdir+'\\'+str(file)
            file_list.append(filepath)
    
#    for i in range(len(file_list)):
#    trackno=random.randint(1,14)
    csv_reader=csv.reader(open(file_list[5]))
    data=[]
    for row in csv_reader:
        row[0]=row[0].replace('(','')
        row[1]=row[1].replace(')','')
        data.append(row)
            
    data_df=DataFrame(data)

    return data_df

#
#def wgn(x,snr):
#　　 snr=pow(10,(snr/10.0))
#　　 xpower = np.sum(x**2)/len(x)
#　　 npower = xpower / snr
#　　 return np.random.randn(len(x)) * np.sqrt(npower)



#def add_random_noise(series):
    
#%%

    

if __name__=='__main__':
    rootdir = "f:\geetest"
    data_df=get_track(rootdir)
    x_series=pd.to_numeric(data_df[0])
    y_series=pd.to_numeric(data_df[1])
    t_series=pd.to_numeric(data_df[2])
    new_x_series=process_series(x_series,length=250)
    new_y_series=process_y(y_series)
#    sum_x=new_x_series.sum(axis=0)
    new_t_series=process_time(t_series)
    
    