#!/usr/bin/env python
# -*- coding:utf-8 -*
"""

"""
import logging

from jieba_analysis._compat import *
import jieba
# import cx_Oracle as oracle
import pymysql
import traceback
import time
import re
from snownlp import SnowNLP

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y-%m-%d-%H%M', time.localtime(time.time()))
rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
logfile = os.path.dirname(os.getcwd()) + '/logs/' + rq + '.log'
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.INFO)  # 输出到file的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # 输出到console的log等级的开关
ch.setFormatter(formatter)

# 第四步，将logger添加到handler里面
logger.addHandler(ch)
logger.addHandler(fh)

# 自定义词典
USER_DICT_NAME = "userdict.txt"

# 加载词典
jieba.load_userdict(get_module_res(USER_DICT_NAME))


def userdictlist(filepath):
    f_name = resolve_filename(filepath)
    userdict = [line.strip() for line in open(f_name, 'r', encoding='utf-8').readlines()]
    return userdict


userdict = userdictlist(get_module_res(USER_DICT_NAME))

# print(userdict)
print(len(userdict))

print(type(userdict))

# 停用词
STOPWORDS_NAME = "stopwords.txt"


# def stopwordslist(filepath):
#     f_name = resolve_filename(filepath)
#     stopwords = [line.strip() for line in open(f_name, 'r', encoding='utf-8').readlines()]
#     return stopwords
#
#
# stopwords = stopwordslist(get_module_res(STOPWORDS_NAME))
#
#
# # 编号名称对应字典
def loadstockname():
    code_name = {}
    with open(resolve_filename(get_module_res("stockcode2namedict.txt")), 'r', encoding='utf-8') as f:
        code_name = eval(f.read())

    all_code_name = {}
    for storkcode in code_name:
        stockname = code_name[storkcode]
        all_code_name[storkcode] = stockname
        all_code_name[stockname] = stockname

    return all_code_name


stockcode2namedict = loadstockname();
print(stockcode2namedict)


def getConn():
    conn = pymysql.connect("10.129.129.156", "mbi", "zxcvb", "spider", charset="utf8")

    return conn


def getGpinfo():
    # 建立数据库连接
    conn = getConn()
    # 创建cursor
    cursor = conn.cursor()

    # 拼接参数
    cursor.execute('''
SELECT DISTINCT symbol,NAME FROM spider_gpinfo WHERE dt > DATE_ADD(CURDATE() ,INTERVAL  -7 DAY)
ORDER BY symbol
                ''')

    # 获取所有数据
    data = cursor.fetchall()

    userdict =[]
    all_code_name = {}
    for row in data:
        userdict.append(row[0][2:])
        userdict.append(row[1])
        all_code_name[row[0][2:]] = row[1]
        all_code_name[row[1]] = row[1]



    # 关闭链接
    cursor.close()
    conn.close()


    print(userdict)
    print("==============")
    print(all_code_name)

    return data

getGpinfo();