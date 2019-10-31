#!/usr/bin/env python
# -*- coding:utf-8 -*
"""

"""
import logging
import os
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



######################################################################################################################
# # 自定义词典
# USER_DICT_NAME = "userdict.txt"
#
# # 加载词典
# jieba.load_userdict(get_module_res(USER_DICT_NAME))
#
# def userdictlist(filepath):
#     f_name = resolve_filename(filepath)
#     userdict = [line.strip() for line in open(f_name, 'r', encoding='utf-8').readlines()]
#     return userdict
# userdict = userdictlist(get_module_res(USER_DICT_NAME))



#编号名称对应字典
# def loadstockname():
#     code_name = {}
#     with open(resolve_filename(get_module_res("stockcode2namedict.txt")), 'r', encoding='utf-8') as f:
#         code_name = eval(f.read())
#
#     all_code_name ={}
#     for storkcode in code_name:
#         stockname = code_name[storkcode]
#         all_code_name[storkcode] = stockname
#         all_code_name[stockname] = stockname
#
#     return all_code_name
#
# stockcode2namedict = loadstockname();

######################################################################################################################
# 停用词
STOPWORDS_NAME = "stopwords.txt"

def stopwordslist(filepath):
    f_name = resolve_filename(filepath)
    stopwords = [line.strip() for line in open(f_name, 'r', encoding='utf-8').readlines()]
    return stopwords

stopwords = stopwordslist(get_module_res(STOPWORDS_NAME))

######################################################################################################################
#从db加载词库

userdict =[]
stockcode2namedict = {}

def load_user_dict():
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

    for row in data:
        jieba.add_word(row[0][2:])
        jieba.add_word(row[1])
        userdict.append(row[0][2:])
        userdict.append(row[1])
        stockcode2namedict[row[0][2:]] = row[1]
        stockcode2namedict[row[1]] = row[1]

    # 关闭链接
    cursor.close()
    conn.close()

######################################################################################################################


def getConn():
    conn = pymysql.connect("10.129.129.156", "mbi", "zxcvb", "spider", charset="utf8")
    return conn

def getIdList():
    # 建立数据库连接
    #conn = pymysql.connect("10.129.128.40", "mbi", "zxcvb", "spider", charset="utf8")
    conn = getConn()

    # 创建cursor
    cursor = conn.cursor()

    # 拼接参数
    # cursor.execute('select autoid,wx_name,wx_id,wx_content from (SELECT autoid,wx_name,wx_id,wx_content FROM SPIDER_ARTICLE order by autoid) where autoid not in(456,516,523) and wx_name is not null and wx_id is not null and autoid=:1 ',(id,))
    cursor.execute('''
SELECT
  autoid
FROM spider_article_quchong
WHERE
wx_name IS NOT NULL
AND wx_id IS NOT NULL
AND wx_id <> ""
AND wx_name <> ""
AND real_publish_time IS NOT NULL
AND autoid > ( SELECT
                  IF ( MAX(article_id) IS NULL,0,MAX(article_id)) AS maxid
                FROM spider_article_fenci )
ORDER BY autoid  desc              
                ''')

    # 获取所有数据
    data = cursor.fetchall()

    # 关闭链接
    cursor.close()
    conn.close()

    return data


#根据文章内容 先分句子，找出每个句子对应的关键词和句子内容
def split_words(wx_content):
    
    sentences = re.split('(。|！|\!|\.|？|\?)',wx_content)
    result ={}
    for s in sentences:
        fenci = jieba.cut(s, cut_all=False, HMM=True)
        for word in fenci:
            if word not in stopwords:
                if dict(stockcode2namedict).__contains__(word):
                    word = stockcode2namedict[word]
                    #结果里面已经包含了改关键字
                    if(dict(result).__contains__(word)):
                        result[word] = result[word] +'\r' +s
                    else:
                        result[word] = s
                            
    return result

#根据文章内容 先分句子，找出每个句子对应的关键词和句子内容
def compute_sentence_sens(result):
    sens ={}
    for k in result:
        s = SnowNLP(result[k])
        sens[k] = s.sentiments
                            
    return sens


def stock_count(split_article,userdict):
    stock_dict = {}
    for word in split_article.strip().split(" "):
        if word in userdict:
            if dict(stock_dict).__contains__(word):
                stock_dict[word] += 1
            else:
                stock_dict[word] = 1
    return stock_dict



def load_spide_article(id):
    """
    https://wenku.baidu.com/view/4dd658294b73f242336c5fa9.html
    从188读数据
    :return: file
    """
    # 建立数据库连接    
    conn = getConn()

    # 创建cursor
    cursor = conn.cursor()

    # 拼接参数
    # cursor.execute('select autoid,wx_name,wx_id,wx_content from (SELECT autoid,wx_name,wx_id,wx_content FROM SPIDER_ARTICLE order by autoid) where autoid not in(456,516,523) and wx_name is not null and wx_id is not null and autoid=:1 ',(id,))
    cursor.execute('''
SELECT
  autoid,
  wx_name,
  wx_id,
  wx_content,
  wx_title,
  real_publish_time
FROM spider_article_quchong
WHERE 
 autoid=%s ''',(id,))

    # 获取所有数据
    data = cursor.fetchall()

    # 计算stock词频
    for article in data:
        stotal = SnowNLP(article[3])
        wx_total_score = stotal.sentiments
        
        print('总情感' , wx_total_score)
        
        stitle = SnowNLP(article[4])
        wx_title_score = stitle.sentiments
        
        print('标题情感' , wx_title_score)
        
        r= split_words(article[3])
        
        print(r)
        sens = compute_sentence_sens(r)
        print(sens)
        
        wx_name = article[1]
        wx_title =article[4]
        real_publish_time= article[5]
        print(real_publish_time)
        
        if sens:
            for k in r:
                params_list_tuple = []
                #参数 
                cishu = len( r[k].split('\r'))
                params_list_tuple.append((article[0], k, cishu, wx_name,wx_title,real_publish_time,   r[k],  sens[k], wx_total_score, wx_title_score))

                sql_roleinfo = '''replace into spider_article_fenci
                (article_id, keywords, cishu ,  wx_name, wx_title, real_publish_time,    wx_sentence,  wx_sentence_score,wx_total_score, wx_title_score ) 
                values(%s,%s,%s,    %s,%s,%s,     %s,            %s, %s, %s   )'''
                
                cursor.executemany(sql_roleinfo, params_list_tuple)
#                 cursor.executemany(sql_roleinfo, article[0], k, cishu, wx_name,wx_title,real_publish_time,   sens[k], wx_total_score, wx_title_score)
                conn.commit()
        
#         article_dict = stock_count(split_words(article[3],stopwords), userdict)
#         # 判断关键词字典不为空时
#         if article_dict:
#             # 拼接params
#             params_list_tuple = []
#             for key in article_dict.keys():
#                 params_list_tuple.append((article[0],key,article_dict[key],   article[1], article[4],article[5]    ))
# 
#             # sql_roleinfo = 'merge into SPIDER_ARTICLE_FENCI u using (select :1 as article_id,:2 as keywords,:3 as cishu from dual)t on (u.article_id = t.article_id and u.keywords = t.keywords) when not matched then insert(article_id,keywords,cishu) values(t.article_id,t.keywords,t.cishu)'
#             sql_roleinfo = 'replace into spider_article_fenci(article_id,keywords,cishu,  wx_name, wx_title, real_publish_time ) values(%s,%s,%s, %s,%s,%s)'
#             # 将词频入库
#             cursor.executemany(sql_roleinfo, params_list_tuple)
#             conn.commit()

    # 获取游标的字段名
    # title = [i[0] for i in cursor.description]

    # 关闭链接
    cursor.close()
    conn.close()

    return data




def update_shuoshidate():
    """
    更新说事情时间
    """
    # 建立数据库连接    
    conn = getConn()

    # 创建cursor
    cursor = conn.cursor()

    # 拼接参数
    # cursor.execute('select autoid,wx_name,wx_id,wx_content from (SELECT autoid,wx_name,wx_id,wx_content FROM SPIDER_ARTICLE order by autoid) where autoid not in(456,516,523) and wx_name is not null and wx_id is not null and autoid=:1 ',(id,))
    cursor.execute('''
UPDATE spider_article_fenci SET
shuoshi_date = IF( DATE_FORMAT(real_publish_time,'%H') < '15', DATE_FORMAT(real_publish_time,'%Y-%m-%d') ,   DATE_ADD(  DATE_FORMAT(real_publish_time,'%Y-%m-%d') , INTERVAL 1 DAY )  ) 
WHERE shuoshi_date IS NULL

 ''')
    conn.commit()
    print("更新shuoshi时间完毕")
    # 关闭链接
    cursor.close()
    conn.close()
    


def update_symbol():
    """
    更新说事情时间
    """
    # 建立数据库连接
    conn = getConn()
    # 创建cursor
    cursor = conn.cursor()

    # 拼接参数
    # cursor.execute('select autoid,wx_name,wx_id,wx_content from (SELECT autoid,wx_name,wx_id,wx_content FROM SPIDER_ARTICLE order by autoid) where autoid not in(456,516,523) and wx_name is not null and wx_id is not null and autoid=:1 ',(id,))
    cursor.execute('''
UPDATE spider_article_fenci t
SET symbol = (SELECT
                gp.symbol
              FROM spider_gpinfo gp
              WHERE gp.name = t.keywords LIMIT 1)
WHERE t.symbol IS NULL              

 ''')
    conn.commit()
    print("更新编码完毕")
    # 关闭链接
    cursor.close()
    conn.close()





##################################################################
#main 主程序
load_user_dict();
data = getIdList();

for autoid in data:
    try:
        articles = load_spide_article(autoid)
        print(autoid, ":Ok")
    except  Exception as e:
        print(autoid,":Exception")
        traceback.print_exc()
        continue

update_shuoshidate();
update_symbol();

    




