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
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
# 功能:解析可还债网页
def HTML(url,time_,time_str):
    gupiao_list = []
    try:
        # 解析网页
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
    except Exception as e:
        print("wrong:" + e)
        pass
    pat = re.compile("\[\{.*?\}\]")
    data = pat.findall(html)
    # 转换为json格式
    js = json.loads(data[0])
    # 循环写入数据
    for i in range(len(js)):
        # print(js[i])
        if js[i]["LISTDATE"] != "-":
            print(str(js[i]["BONDCODE"]))
            time.sleep(1)
            lilv,jinkia,zhenfu,zuigao,zuidi,zuoshou,chengjiaoliang,chengjiaoe =get_data(str(js[i]["BONDCODE"]),time_)
            print( lilv, jinkia, zhenfu, zuigao, zuidi, zuoshou, chengjiaoliang, chengjiaoe)
            list = [lilv, jinkia, zuigao,zuidi,zuoshou]
            if lilv>1000:
                lilv = lilv /10
            if jinkia > 1000:
                jinkia = jinkia / 10
            if zuigao > 1000:
                zuigao = zuigao / 10
            if zuidi > 1000:
                zuidi = zuidi / 10
            if zuoshou > 1000:
                zuoshou = zuoshou / 10

            # time.sleep(1)
            data=(js[i]["SNAME"], js[i]["BONDCODE"], js[i]["CORRESCODE"], js[i]["STARTDATE"],lilv,jinkia,zhenfu,zuigao,zuidi,zuoshou,chengjiaoliang,chengjiaoe)
            gupiao_list.append(data)
    title = ["债券简称","债券代码", "正股代码","上市时间","现价","今开","振幅","最高","最低","昨收","成交量","成交额"]
    df = pd.DataFrame(gupiao_list, columns=title)
    to_csv(df, f"id{time_str}.csv")

# 保存csv格式的文件夹
def to_csv(df, csv_file):
    if os.path.exists(csv_file) == False:
        df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, mode='a+', header=False, index=False)


# 获取每个可还债的数据
# 输入:可还债id,与时间
# 输出:"现价","今开","振幅","最高","最低","昨收","成交量","成交额" 的数据
def get_data(id,time_):
    url ="http://push2.eastmoney.com/api/qt/stock/get?secid=1."+str(id)+"&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172,f182,f191,f192,f532&cb=jQuery1124021434030444820706_"+str(time_)+"000"+"&type=CT&cmd=1280922&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_="+str(time_)+"000"
    # url = "http://push2.eastmoney.com/api/qt/stock/get?secid=1."+str(id)+"&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172,f182,f191,f192,f532&cb=jQuery1124002590768518466602_1588042202265&type=CT&cmd=1230442&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_=1588042202266"
    print(url)
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
    except Exception as e:
        print("wrong:" + e)
    print(html)
    try:
        try:
            # 获取内容
            list_ = []
            pat = re.compile("({.*?\})")
            data = pat.findall(html+"}}")
            d =eval(data[0]+"}")
            new_data = d.get("data")
            # print(new_data)
            lilv= new_data.get("f43") # 利率
            jinkia = new_data.get("f46") # 今开
            zhenfu=new_data.get("f171") # 振幅
            zuigao = new_data.get("f44") # 最高
            zuidi = new_data.get("f45") # 最低
            zuoshou = new_data.get("f60") # 昨收
            chengjiaoliang = new_data.get("f47")
            chengjiaoe = new_data.get("f48")
            return round(float(lilv)/100,2), round(float(jinkia)/100,2), str(round(float(zhenfu),2)) +"%", round(float(zuigao)/100,2), round(float(zuidi)/100,2), round(float(zuoshou)/100,2), chengjiaoliang, chengjiaoe
        except:
            print("*" * 100)
            # url = "http://push2.eastmoney.com/api/qt/stock/get?secid=0." + str(
            #     id) + "&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172,f182,f191,f192,f532&cb=jQuery1124021434030444820706_" + str(
            #     time_) + "000" + "&type=CT&cmd=1280922&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_=" + str(
            #     time_) + "000"
            url = "http://push2.eastmoney.com/api/qt/stock/get?secid=1." + str(
                id) + "&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172,f182,f191,f192,f532&cb=jQuery1124021434030444820706_" + str(
                time_) + "000" + "&type=CT&cmd=1280922&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_=" + str(
                time_) + "000"
            try:
                r = requests.get(url, headers=headers, timeout=30)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                html = r.text
            except Exception as e:
                print("wrong:" + e)
            # print(html)
            pat = re.compile("({.*?\})")
            data = pat.findall(html + "}}")
            d = eval(data[0] + "}")
            new_data = d.get("data")
            lilv = new_data.get("f43")  # 利率
            jinkia = new_data.get("f46")  # 今开
            zhenfu = new_data.get("f171")  # 振幅
            zuigao = new_data.get("f44")  # 最高
            zuidi = new_data.get("f45")  # 最低
            zuoshou = new_data.get("f60")  # 昨收
            chengjiaoliang = new_data.get("f47")
            chengjiaoe = new_data.get("f48")
            # print( lilv, jinkia, zhenfu, zuigao, zuidi, zuoshou, chengjiaoliang, chengjiaoe)
            return round(float(lilv)/100,2), round(float(jinkia)/100,2), str(round(float(zhenfu),2)) +"%", round(float(zuigao)/100,2), round(float(zuidi)/100,2), round(float(zuoshou)/100,2), chengjiaoliang, chengjiaoe
    except:
        return  0,0,0,0,0,0,0,0

import time
# 获取可还债网页的所有内容
# 输入:时间类型
# 输出: csv文件
def main(time_,time_str):
    for i in range(1, 9):
        url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB2.0&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=" + str(
            i) + "&ps=50&js=var%20GCPJwVrm={pages:(tp),data:(x),font:(font)}&rt=52919237"
        print(url)
        HTML(url,time_,time_str)
        time.sleep(2)

# 字符类型的时间:
def get_time(time_str):
    # 转为时间数组
    timeArray = time.strptime(time_str, "%Y%m%d")
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

if __name__ == '__main__':
    # 获取当前时间
    for time_str in ["20200426"]:
        time_ = get_time(time_str)
        print("时间戳",time_)
        # 主程序入口
        main(time_,time_str)
