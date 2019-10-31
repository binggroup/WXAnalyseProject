# -*- coding: utf-8 -*-

# 随机森林预测流失
import pandas as pd
import time
import os
# from sklearn.tree import DecisionTreeClassifier
# from matplotlib.pyplot import *
# from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
# from sklearn.externals.joblib import Parallel, delayed
# from sklearn.tree import export_graphviz
import warnings
# from sklearn import cross_validation
# from sklearn import metrics

import logging
import logging.config

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
# rq = time.strftime('%Y-%m-%d-%H%M', time.localtime(time.time()))
rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
print('当前目录：' + os.getcwd())
logfile = os.getcwd() + '/logs/' + rq + '.log'
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

warnings.filterwarnings("ignore")

# 参数初始化
train_file = './data/train/foundation/cym_tlbb_ls_2016-04-01.txt'
# train_file = '/home/yingyong/datamining/R/train/foundation/cym_tlbb_ls_2016-04-01.txt'

data = pd.read_csv(train_file, sep=',', nrows=100000, skip_blank_lines=True)  # 导入数据



logger.info("训练集特征数：" + str(len(data.columns)))
logger.info("训练集记录条数：" +  str(data.shape[0]) )
logger.info(data.columns.tolist())
# logger.info("前10行的数据为：")
# logger.info(data.head(10))
#去除数据中的null
# df["VIN"]=df["VIN"].apply(lambda x: np.NaN if str(x).isspace() else x)
# data['last_logout_interval_day'] = data['last_logout_interval_day'].apply(lambda x: 31 if x.isnull else x)
# data['last_1day_day'] = data['last_1day_day'].apply(lambda x: 0 if pd.isna(x) else x)
# data['last_1day_day'] = 0 if pd.isna(data['last_1day_day']) else data['last_1day_day']

#每一列的默认值替换null nan
default_values={
    'last_logout_interval_day' : 31,
    'lv' : 1,
    'ls2' : 0, 'ls3' :0,
        'last_3day_day' :0, 'last_3day_time' :0,
        'last_1day_day' : 0, 'last_1day_time' : 0,
        'last_2day_day' : 0,  'last_2day_time' : 0,
        'last_3day_day' : 0, 'last_3day_time' :0,
        'consume1' : 0 , 'consume1_day' :0,
        'consume1_cishu' : 0,
        'consume2': 0, 'consume2_day' :0,
        'consume4' : 0,  'consume4_day' :0,
        'yuanbaocost' : 0,
        'recharge1' : 0, 'recharge1_cishu' :0, 'recharge1_day' :0,
        'recharge2' : 0, 'recharge2_day' :0,
        'recharge4' :0 , 'recharge4_day' :0
    }

def preprocess(d):
    d.fillna(value=default_values, inplace=True)
    # 追加新的列判断趋势
    d['consume_cr'] = d['consume1'] < d['consume2']
    d['consume_day_cr'] = d['consume1_day'] < d['consume2_day']
    d['recharge_cr'] = d['recharge1'] < d['recharge2']
    d['recharge_day_cr'] = d['recharge1_day'] < d['recharge2_day']
    d['day_cr'] = d['last_3day_day'] < d['last_1day_day']
    d['time_cr'] = d['last_3day_time'] < d['last_1day_time']
    #从数据中定义流失标签
    d['ls']=0
    #ls2  dt日期以后1~2天登录的天数  未来1~2天未登录则认为流失
    d.loc[d['ls2'] <=0 , 'ls'] = 1

preprocess(data)



#去除不要的行
x_train=data.loc[data['vip'] >=8]
y_target=x_train['ls']

#去除不要的列
x_train.drop(['ls3', 'ls2', 'roleid', 'userid', 'ls'], axis=1, inplace=True)



logger.info(x_train.shape)

logger.info('开始模型训练...')
rfc = RandomForestClassifier(n_estimators=100, max_depth=None, min_samples_split=2, random_state=0)
rfc.fit(x_train, y_target)

logger.info('模型训练结束...')
score = rfc.score(x_train , y_target)
logger.info(u'评估模型准确率:')
logger.info(score)

logger.info('特征权重：')
cols = data.columns.values
s=''
for index in range(x_train.shape[1]):
    s = s + str( round( rfc.feature_importances_[index],3)) + ','
logger.info(s)



# logger.info( str(cols[index]) + '=' + str(rfc.feature_importances_[index]))
#预测
# r=rfc.predict(x_train)
# from sklearn.metrics import confusion_matrix
# cm = confusion_matrix( y_target,r)
# logger.info('混淆矩阵：')
# logger.info(cm)


# rframe= pd.DataFrame(r,columns=['yucejieguo'])
# temp = pd.concat([rframe,y_target],axis=1)
# temp.to_csv('./data/temp.txt')


###################################################################
#载入实际数据

# # real_file = './data/cym_tlbb_ls_2011-04-09.txt'
# real_file = '/home/yingyong/datamining/R/test/bak/foundation/cym_tlbb_ls_2019-08-11.txt'
#
#
# realdata = pd.read_csv(real_file,sep=',', nrows=100000,skip_blank_lines=True) #导入数据
# preprocess(realdata)
#
# #去除不要的行，只预测vip 8以上的
# xx_train=realdata.loc[ realdata['vip'] >=8 ]
#
# # df_result =pd.DataFrame( xx_train['roleid'], columns=['roleid'])
# df_result= xx_train[['roleid','last_1day_day','last_2day_day']]
#
# #去除不要的列
# xx_train.drop(['ls3', 'ls2', 'roleid', 'userid', 'ls'], axis=1, inplace=True)
# predicted = rfc.predict(xx_train)
# prob = rfc.predict_proba(xx_train)
#
#
#
#
#
# df_predicted= pd.DataFrame(predicted,columns=['predict_ls'])
# df_prob= pd.DataFrame(prob)
# print(type(df_result))
# print(type(df_predicted))
# print(type(df_prob))
# result = pd.concat([ df_result, df_predicted ],axis=1)
# result = pd.concat([ df_result, df_prob ],axis=1)
# print(result.head(10))
# #
# result.to_csv('/home/yingyong/datamining/R/test/bak/result.20190811.txt')



