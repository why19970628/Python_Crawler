# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = '强子'
import requests
from settings import *
import cons

dict_station = {}
for i in cons.station.split('@'):
    tmp_list = i.split('|')
    #print(tmp_list)
    if len(tmp_list) > 2:
        dict_station[tmp_list[1]] = tmp_list[2]
print(dict_station)

from_station = dict_station[FROM_STATION]
to_station = dict_station[TO_STATION]
print(from_station,to_station)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def queryTicket():#query_ticket
    url='https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date='+TRAIN_DATE+'&leftTicketDTO.from_station='+from_station+'&leftTicketDTO.to_station='+to_station+'&purpose_codes=ADULT'
    print(url)
    response = requests.get(url=url,headers=headers,verify=False)
    result = response.json()
    print(result['data']['result'])
    print(TRAIN_DATE,FROM_STATION,TO_STATION)
    print('车次 '+' 座位 '+' 有无票'+' 票数')
    return result['data']['result']

n = 0
'''
23 = 软卧
28 = 硬卧
3 = 车次
29=硬座
'''

for i in queryTicket():
    tmp_list = i.split('|')
    #for ii in tmp_list:
    #    print(n)
    #     print(ii)
     #    n += 1
    set = tmp_list[29]
    set1 = tmp_list[23]
    if set == '' or set == '无':
        print(tmp_list[3],'硬座 '+'无票',tmp_list[29])

    else:
        print(tmp_list[3],'硬座 '+'有票',tmp_list[29])
        #下单