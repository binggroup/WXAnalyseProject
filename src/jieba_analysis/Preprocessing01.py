#!/usr/bin/env python
# -*- coding:utf-8 -*
"""
 数据处理，可以参考《自然语言处理时，通常的文本清理流程是什么？》
 以英文文本处理为例。大致分为以下几个步骤：
    1. Normalization
        标准化：字母小写转换、标点符号处理等，英文里通常只要A-Za-z0-9，根据实际情况确定处理
    2. Tokenization
        Token 是“符号”的高级表达。一般指具有某种意义，无法再分拆的符号。就是将每个句子分拆成一系列词，英文里词之间天然有空格。
    3. Stop words
        Stop Word 是无含义的词，例如'is'/'our'/'the'/'in'/'at'等。它们不会给句子增加太多含义，单停止词是频率非常多的词。 为了减少我们要处理的词汇量，从而降低后续程序的复杂度，需要清除停止词。
    4. Part-of-Speech Tagging   词性标注
    5. Named Entity Recognition 命名实体
    6. Stemming and Lemmatization  将词的不同变化和变形标准化
"""
import logging
from jieba_analysis._compat import *
import jieba
import cx_Oracle as oracle
import traceback



logger = logging.getLogger(__name__)

# 自定义词典
USER_DICT_NAME = "userdict.txt"

# 加载词典
jieba.load_userdict(get_module_res(USER_DICT_NAME))

def userdictlist(filepath):
    f_name = resolve_filename(filepath)
    userdict = [line.strip() for line in open(f_name, 'r', encoding='utf-8').readlines()]
    return userdict
userdict = userdictlist(get_module_res(USER_DICT_NAME))

# 停用词
STOPWORDS_NAME = "stopwords.txt"

def stopwordslist(filepath):
    f_name = resolve_filename(filepath)
    stopwords = [line.strip() for line in open(f_name, 'r', encoding='utf-8').readlines()]
    return stopwords

stopwords = stopwordslist(get_module_res(STOPWORDS_NAME))

def split_words(file,stopwords):
    """
    参考：https://github.com/fxsjy/jieba
    :param file:文件
    :return:
    """
    result = ''
    split_file = jieba.cut(file, cut_all=False, HMM=True)
    for word in split_file:
        if word not in stopwords:
            if word!='\t':
                result += word
                result += " "
    return result

def load_spide_article(id):
    """
    https://wenku.baidu.com/view/4dd658294b73f242336c5fa9.html
    从188读数据
    :return: file
    """
    # 连接数据库
    db = oracle.connect('mbi/zxcvb@10.129.129.188:1521/mbidev')

    # 创建cursor
    cursor = db.cursor()

    # 拼接参数
    cursor.execute('select autoid,wx_name,wx_id,wx_content from (SELECT autoid,wx_name,wx_id,wx_content FROM SPIDER_ARTICLE order by autoid) where autoid not in(456,516,523) and wx_name is not null and wx_id is not null and autoid=:1 ',(id,))

    # 获取所有数据
    data = cursor.fetchall()
    # 计算stock词频
    for article in data:
        article_dict = stock_count(split_words(article[3],stopwords), userdict)

        # 判断关键词字典不为空时
        if article_dict:
            # 拼接params
            params_list_tuple = []
            for key in article_dict.keys():
                # print(key)
                params_list_tuple.append((article[0],key,article_dict[key]))

            sql_roleinfo = 'merge into SPIDER_ARTICLE_FENCI u using (select :1 as article_id,:2 as keywords,:3 as cishu from dual)t on (u.article_id = t.article_id and u.keywords = t.keywords) when not matched then insert(article_id,keywords,cishu) values(t.article_id,t.keywords,t.cishu)'
            # 将词频入库
            cursor.executemany(sql_roleinfo, params_list_tuple)
            db.commit()

    # 获取游标的字段名
    # title = [i[0] for i in cursor.description]

    # 关闭链接
    cursor.close()
    db.close()

    return data

def stock_count(split_article,userdict):
    stock_dict = {}
    for word in split_article.strip().split(" "):
        if word in userdict:
            if dict(stock_dict).__contains__(word):
                stock_dict[word] += 1
            else:
                stock_dict[word] = 1
    return stock_dict



for i in range(19810,30162):
#     articles = load_spide_article(i)
#     print(i,"ok")
    
    try:
        articles = load_spide_article(i)
        print(i,":ok")
    except Exception:
        print(i,":Exception")
        print( 'str(Exception):\t', str(Exception))
        continue
    
# print(split_words(articles[2],stopwords))

# test
# for i in articles:
#     dicts = stock_count(split_words(i[3],stopwords),userdict)
#     print(dicts)



