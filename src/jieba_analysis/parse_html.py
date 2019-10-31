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
from  lxml import etree

import json
import jsonpath

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y-%m-%d-%H%M', time.localtime(time.time()))
rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
logfile  = os.path.dirname(os.getcwd()) + '/logs/' + rq + '.log'
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




#全局连接
conn = pymysql.connect("10.129.129.156", "mbi", "zxcvb", "spider", charset="utf8")

# def getConn():
#     conn = pymysql.connect("10.129.129.156", "mbi", "zxcvb", "spider", charset="utf8")
#     return conn

def get_spider_wx_list():
    # 建立数据库连接
    # conn = getConn()

    # 创建cursor
    cursor = conn.cursor()

    # 拼接参数
    cursor.execute('''
SELECT
    url, headers, MID,request_body,response_body,autoid,insert_time,file_id,process_status  
FROM spider_wx 
    where autoid > 15490 and process_status IS NULL order by autoid 
                ''')

    # 获取所有数据
    data = cursor.fetchall()
    #解析列头信息
    col={}
    des = cursor.description
    i = 0
    for field in des:
        col[field[0].lower()] = i
        i=i+1

    # 关闭链接
    cursor.close()
    # conn.close()

    return data,col


def update_mid():
    """
        更新mid
    """
    # 建立数据库连接
    # conn = getConn()

    # 创建cursor
    cursor = conn.cursor()
    print("开始更新mid")

    # 拼接参数
    cursor.execute('''
    UPDATE spider_wx SET MID=  SUBSTR(headers, INSTR(headers,'&mid=') +4,12)	WHERE INSTR(headers,'&mid=') > 1 AND mid is null
     ''')
    conn.commit()
    print("更新mid完毕")
    # 关闭链接
    cursor.close()
    # conn.close()

# '''
# url
# headers
# MID
# request_body
# response_body
# autoid
# insert_time
# file_id
# process_status
#
# '''

def parse_html(data,col):
    for orihtml in data:
        autoid =orihtml[col['autoid']]
        url = orihtml[col['url']]
        mid = orihtml[col['mid']]
        response_body = orihtml[col['response_body']]
        try:
            # articles = load_spide_article(autoid)
            if url.startswith('mp.weixin.qq.com/s'):
                process_html_content(autoid,mid,response_body)

            if url.startswith('mp.weixin.qq.com/mp'):
                process_json_content(autoid,mid,response_body)

        except  Exception as e:
            print(autoid,":Exception")
            traceback.print_exc()
            continue

        print('ok')

def update_process_status(autoid):
    """
        更新mid
    """
    # 建立数据库连接
    # conn = getConn()

    # 创建cursor
    cursor = conn.cursor()

    # 拼接参数
    cursor.execute('''
    update  spider_wx    set process_status = 'ok'    where  autoid = %s
     ''',[(autoid)] )
    conn.commit()
    print("更新mid完毕")
    # 关闭链接
    cursor.close()
    # conn.close()

def process_json_content(autoid,mid,response_body):
    jsonobj = json.loads(response_body)

    read_num =0
    temp= jsonpath.jsonpath(jsonobj, '$.appmsgstat.read_num')
    if temp:
        read_num=temp[0]

    print('read_num:')
    print(read_num)

    like_num = jsonpath.jsonpath(jsonobj, '$.appmsgstat.like_num')[0]
    print('like_num')
    print(like_num)

    real_read_num = jsonpath.jsonpath(jsonobj, '$.appmsgstat.real_read_num')[0]
    print('real_real_num')
    print(real_read_num)

    reward_total_count = 0
    temp = jsonpath.jsonpath(jsonobj, '$.reward_total_count')
    if temp:
        reward_total_count = temp[0]
    print('reward:')
    print(reward_total_count)

    insert_spider_wx_statinfo(read_num,  like_num,  real_read_num,  reward_total_count, mid)
    update_process_status(autoid)

    pass

def insert_spider_wx_statinfo(read_num,  like_num,  real_read_num,  reward_total_count, mid):
    sql ='''
    INSERT INTO spider_wx_statinfo (read_num,  like_num,  real_read_num,  reward_total_count, mid )
    VALUES
                                    (%s,       %s,         %s,             %s,                %s )

    '''

    # 建立数据库连接
    # conn = getConn()
    # 创建cursor
    cursor = conn.cursor()


    params_list_tuple = []
    # 参数
    params_list_tuple.append( (read_num,  like_num,  real_read_num,  reward_total_count, mid) )
    print(params_list_tuple)
    cursor.executemany(sql, params_list_tuple)

    conn.commit()
    print("更新shuoshi时间完毕")
    # 关闭链接
    cursor.close()
    # conn.close()

def insert_spider_article(wx_name,  wx_id,  wx_title,  wx_content,  publish_time,     real_publish_time, mid):
    sql ='''
    INSERT INTO spider_article (wx_name,  wx_id,  wx_title,  wx_content,  publish_time,     real_publish_time, mid,   spide_time )
    VALUES
                               (%s,       %s,     %s,        %s,          %s ,              %s,                %s,     now()    )

    '''

    # 建立数据库连接
    # conn = getConn()

    # 创建cursor
    cursor = conn.cursor()


    params_list_tuple = []
    # 参数
    params_list_tuple.append( (wx_name,  wx_id,  wx_title,  wx_content,  publish_time,     real_publish_time, mid) )
    print(params_list_tuple)
    cursor.executemany(sql, params_list_tuple)


    conn.commit()
    print("更新shuoshi时间完毕")
    # 关闭链接
    cursor.close()
    # conn.close()








def process_html_content(autoid,mid,response_body):
    #判断是转发的文章
    if response_body.find('js_share_author') >0:
        return
    if response_body.find('因违规无法查看') >0:
        print('因违规无法查看:' + str(autoid))
        return
    if response_body.find('该内容已被发布者删除') >0:
        print('该内容已被发布者删除:' + str(autoid))
        return
    html = etree.HTML(response_body)

    wx_name = html.xpath('//span[@id="profileBt"]/a/text()')[0].replace(' ','').replace('\n','')
    print(wx_name)

    wx_title = html.xpath('//h2[@id="activity-name"]/text()')[0].replace(' ', '').replace('\n', '')
    print(wx_title)

    #默认微信id = 微信name
    wx_id = wx_name
    tempobj =html.xpath("//p[@class='profile_meta'][1]/span[@class='profile_meta_value']/text()")
    if tempobj:
        wx_id= tempobj[0].replace(' ', '').replace('\n', '')

    print(wx_id)

    ori_wx_content = html.xpath("//div[@id='js_content']//text()")
    wx_content = ''.join(ori_wx_content).replace(' ', '').replace('\n', '')

    time_index=response_body.find(" ct=")
    if time_index > 0:
        str_publish_time = response_body[time_index+5 : time_index + 15]
    else:
        time_index = response_body.find('",n="')
        str_publish_time = response_body[time_index + 5: time_index + 15]
        pass
    print(str_publish_time)

    #时间戳转化为字符串格式
    timeArray = time.localtime(int(str_publish_time))
    format_publish_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(format_publish_time)

    insert_spider_article(wx_name,  wx_id,  wx_title,  wx_content,  str_publish_time,     format_publish_time, mid)
    update_process_status(autoid)


    pass




def insert_spider_article_quchong():
    sql_trunc ='''
    TRUNCATE TABLE spider_article_quchong
    '''

    sql = '''
    INSERT INTO spider_article_quchong   
    SELECT    a.autoid,   a.wx_title,   a.wx_name,   a.wx_id,   a.wx_content,   a.publish_time,   a.spide_time,   a.real_publish_time,   a.mid
        FROM (  SELECT  MAX(autoid) AS autoid FROM spider_article WHERE MID IS NOT NULL  GROUP BY MID,wx_name ) aid
        LEFT JOIN spider_article a     ON a.autoid = aid.autoid 
    '''

    # 建立数据库连接
    # conn = getConn()

    # 创建cursor
    cursor = conn.cursor()
    cursor.execute(sql_trunc)
    cursor.execute(sql)
    conn.commit()
    print("写入到去重表")
    # 关闭链接
    cursor.close()
###################################################################################################



#第一步 更新mid
update_mid();
#第二步 获取原始微信文章html内容
data,col = get_spider_wx_list();

#第三步 解析
parse_html(data,col)

#第四步 写入去重表
insert_spider_article_quchong()

#关闭连接
conn.close()

