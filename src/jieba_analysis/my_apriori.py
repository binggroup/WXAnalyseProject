#!/usr/bin/env python
# -*- coding:utf-8 -*
"""

"""

from apyori import apriori

import pandas as pd
import logging
import time
import os
import numpy as np
import traceback



#####################################################

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y-%m-%d-%H%M', time.localtime(time.time()))
rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
logfile  = os.path.dirname(os.getcwd()) + '/logs/' + 'arule' + rq + '.log'
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
#控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # 输出到console的log等级的开关
ch.setFormatter(formatter)

# 第四步，将logger添加到handler里面
logger.addHandler(ch)
logger.addHandler(fh)


#####################################################
 

csvfile='C:/Users/hurenbing/Documents/fupan/arule20190614.csv'

# 
# ff= np.loadtxt(csvfile)
# print(ff)
df=pd.read_csv(csvfile)

# print(df.head())

# a = df.head(15)
a=df
# print(a)

last_keywords =df.at[0,"keywords"]
last_dt=df.at[0,"dt"]
last_key= last_keywords + '_' + last_dt
print(last_key)

alllist=[]
gzh =[]
for index, row in a.iterrows():
    current_kw = row["keywords"]
#     current_dt = row["dt"]
    current_dt = ''
    current_key = current_kw + '_' + current_dt
    if current_key == last_key:
        gzh.append(row["gongzhonghao"])
    else:
        alllist.append(gzh)
        gzh = []
        gzh.append(row["gongzhonghao"])
            
    last_keywords = current_kw
#     last_dt = current_dt
    last_dt = ''
    last_key= last_keywords + '_' + last_dt
print('alllist==============')    
# print(alllist)    
for r in alllist:
    logger.info(r)    

# transactions = [
#     ['beer', 'nuts'],
#     ['beer', 'cheese'],
#     ['beer', 'nuts','abc'],
#     ['beer', 'nuts','abc','cheese'],
#         
# ]
 

apy = apriori(alllist) 
results = list(apy)
 
for r in results:
    if r.support > 0.2:
        print(r.support)
        for c in r.ordered_statistics:
            if c.confidence> 0.6:
                logger.info(c)
                print(c)
#         logger.info(r)
    
#     print (r);
# # print(results)
