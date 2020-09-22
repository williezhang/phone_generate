#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import re
import requests

import pandas as pd


import warnings
warnings.filterwarnings('ignore')





def process_json(result_data):
    """
    处理
    """
    result_data1=''
    for i in range(len(result_data)):
        if result_data[i]=='{' and result_data[i+1]=='i':
            result_data1+=result_data[i]
            result_data1+='"'
        elif result_data[i]=='d' and result_data[i+1]==':':
            result_data1+=result_data[i]
            result_data1+='"'

        elif result_data[i]==',' and result_data[i+1]=='n':
            result_data1+=result_data[i]
            result_data1+='"'
        elif result_data[i]=='e' and result_data[i+1]==':':
            result_data1+=result_data[i]
            result_data1+='"'
        else:
            result_data1+=result_data[i]
    return result_data1





# 所有的id和城市名称数据

def get_all_citys():
    """
    获取所有的城市数据
    :return:
    """

    headers = {
        'authority': 'uutool.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'UM_distinctid=16f759fe6bd24b-0322efd0d180d8-1d376b5b-1aeaa0-16f759fe6beb69; CNZZDATA1275106188=191793625-1578225029-https%253A%252F%252Fwww.google.com%252F%7C1578316721',
    }

    resp = requests.get('https://uutool.cn/assets/js/tools/phone_generate.min.js?v=2', headers=headers).text

    re_rule = r'areaArr:(.+?)segmentArr:'

    # 匹配换行符
    result_data = re.findall(re_rule, resp, re.S)[0].strip()[:-1]

    result = json.loads(process_json(result_data))

    # 获取所有的省份
    provices = result.keys()

    # 所有的城市
    citys = {}

    for provice in provices:
        current_citys = result.get(provice)
        # citys.extend(current_citys)
        for item in current_citys:
            citys[item.get('name')] = item.get('id')

    return citys





def generate_phones(num, areas):
    """
    生成随机号码
    :param num:数目
    :param areas: 区域
    :return: 
    """

    headers = {
        'authority': 'api.uukit.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'enote_app/json, text/javascript, */*; q=0.01',
        'origin': 'https://uutool.cn',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://uutool.cn/phone-generate/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    data = {
        'phone_num': num,
        'area': areas,
        #'segment': '133,153,189,180,181,177,173,139,138,137,136,135,134,159,158,157,150,151,152,147,188,187,182,183,184,178,130,131,132,156,155,186,185,145,176'
        'segment': '133,153,180,138,137,136,135,159,150,151,188,187,130,131,132'

    }

    response = requests.post('https://api.uukit.com/phone/generate_batch', headers=headers, data=data,verify=False)

    phones = json.loads(response.text).get('data').get('rows')

    return phones





def main(city):
    citys=get_all_citys()
    phone=generate_phones(100, citys[city])
    df=pd.DataFrame(phone,columns={'tel'})
    return df



