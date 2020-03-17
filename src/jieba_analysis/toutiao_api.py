#!/usr/bin/env python
# -*- coding:utf-8 -*
"""

"""

# def get_advertiser_stat(access_token):    
#     import requests    
#     open_api_url_prefix = "https://ad.toutiao.com/open_api/"    
#     uri = "2/report/advertiser/get/"    
#     #1629783625375756
#     url = open_api_url_prefix + uri    
#     params = {  "start_date": "2019-06-01", 
#                 "end_date": "2019-06-18",   
#                 "time_granularity": "STAT_TIME_GRANULARITY_DAILY",  
#                 "advertiser_id": "1632137214772235",    }  
#     headers = {"Access-Token": "2f8bc10ccd939830c0ef0f5646d12cda454b5d4e"}    
#     
#     rsp = requests.get(url, json=params, headers=headers)    
#     rsp_data = rsp.json()    
#     return rsp_data
# 
# 
# print("==============begin....")
# a=get_advertiser_stat("")
# print(a)

# token='24_BOq7ZIb70IsVvEjTq_qBeRAU2yz0kuzgA42Oo5B8cHlQwdSM-NULqfKLz_nrlgm3kVZ0d0qzCjuWolk0vj4OKfmId80lJsMa_OP6uahHdLHng8XIku3hVt5LNWLlZSntlMmcSyu5pwPIaSraLRWcAFATZE'
# def get_wx_advertiser_stat(access_token):
#     import requests
#     open_api_url_prefix = "https://api.weixin.qq.com/marketing/user_action_sets/add?version=v1.0&access_token=" + access_token
#     uri = ""
#
#     url = open_api_url_prefix + uri
#     params = {  "type": "IOS",
#                 "mobile_app_id": "wx8fcf309675d53582",
#                 "name": "konggui",
#                 "description": "konggui",    }
#     headers = {"Content-Type": "application/json"}
#     rsp= requests.post(url,data=params,json=None,headers=headers)
#     # rsp = requests.get(url, json=params, headers=headers)
#     rsp_data = rsp.json()
#     return rsp_data
#
# print('=====begin....')
# a=get_wx_advertiser_stat(token)
# print(a)


token='1437425790c59742de530063ff55d02b3efaf5a3'
def get_site():
    import requests
    open_api_url_prefix = "https://ad.oceanengine.com/open_api/"
    uri = "2/tools/site/get/"
    url = open_api_url_prefix + uri
    params = {
        "advertiser_id": 1358625641865981,
        "page": 1,
        "page_size": 20,
    }
    headers = {"Access-Token": token}
    rsp = requests.get(url, json=params, headers=headers)
    rsp_data = rsp.json()
    print(rsp_data)
    return rsp_data

print('begin...')
get_site()

print('end...')
