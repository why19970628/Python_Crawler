import re
import os
import requests
import json
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 5000)

# 字符类型的时间:
def get_time(time_str):
    # 转为时间数组
    timeArray = time.strptime(time_str, "%Y%m%d")
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

# 坐拥: 解析每个网页的数据
# 输入:字符与每个网页所需的地址,请求的参数
# 输出: 网页解析所获得的股票数据
def HTML(time_str,url, params):
    gupiao_list = []
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=30, params=params)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
    except Exception as e:
        print("wrong:" + e)
    # pat = re.compile("\[\{.*?\}\]")
    pat = re.compile("({.*?})")
    data = pat.findall(html)
    # print(data)
    js = []
    for d in data:
        try:
            d1=eval(d+"]}}").get("data").get("diff")[0]
        except:
            d1 = eval(d)
        js.append(d1)
    for i in range(len(js)):
        zhenfu = str(js[i]["f7"]) + "%"
        gupiao_list.append((
            js[i]["f12"], js[i]["f14"], js[i]["f2"], zhenfu, js[i]["f4"], js[i]["f5"], js[i]["f6"],
                            zhenfu, js[i]["f15"], js[i]["f16"], js[i]["f17"], js[i]["f18"], js[i]["f10"]))
    title = ["代码", "名称", "最新价", "涨跌幅", "涨跌额", "成交量", "成交额",
             "振幅", "最高", "最低", "今开", "昨收", "量比"]
    df = pd.DataFrame(gupiao_list, columns=title)
    to_csv(df, f"result_{time_str}.csv")

# 保存csv图片
def to_csv(df, csv_file):
    if os.path.exists(csv_file) == False:
        df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, mode='a+', header=False, index=False)


import time
# 主函数入
# 输入:时间与时间字符
# 输出:解析网页 所需的header请求
def main(time_str,time_):
    time_ = str(time_) +"000"
    # 爬出249个网页
    for i in range(1, 250):
        print(i)
        url = 'http://push2.eastmoney.com/api/qt/clist/get'
        params = {
            'cb': f'jQuery112407955974158503321_{str(time_)}',
            'pn': str(i),
            'pz': '20',
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23',
            'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
            '_': str(time_)
        }
        # 解析网页入口
        HTML(time_str, url,params)
        # 睡眠
        time.sleep(6)


if __name__ == '__main__':
    # 输入时间
    for time_str in ["20200417"]:
        time_ = get_time(time_str)
        # 程序入口
        main(time_str,time_)
