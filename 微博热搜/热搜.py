# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 09:35:03 2018

@author: dell
"""
## 调用要使用的包
import json
import random
import requests
import time
import pandas as pd
import os
import jieba
from scipy.misc import imread  # 这是一个处理图像的函数
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import datetime
from collections import Counter
os.chdir('D:/爬虫/微博热搜')
## 获得日期
def getBetweenDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y/%m/%d")
    end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y/%m/%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

## 分词
def get_words_list(df):
    df['words_list'] = []
    word_generator = jieba.cut_for_search(df['title'])
    for word in word_generator:
        df['words_list'].append(word)
    return df

## explode
def dataframe_explode(dataframe, fieldname): 
    temp_fieldname = fieldname + '_made_tuple_' 
    dataframe[temp_fieldname] = dataframe[fieldname].apply(tuple)       
    list_of_dataframes = []
    for values in dataframe[temp_fieldname].unique().tolist(): 
        list_of_dataframes.append(pd.DataFrame({
            temp_fieldname: [values] * len(values), 
            fieldname: list(values), 
        }))
    dataframe = dataframe[list(set(dataframe.columns) - set([fieldname]))].merge(pd.concat(list_of_dataframes), how='left', on=temp_fieldname) 
    del dataframe[temp_fieldname]
    return dataframe

## 绘制词云
def draw_word_cloud(word):
    word_title = resou_word[resou_word['title'].str.contains(word)]
    word_title = word_title.groupby(['title'],as_index=False).agg({'searchCount':['max']})
    word_title.columns = ['title','count']
    data = [(word_title['title'][i],word_title['count'][i]/1000000) for i in range(word_title.shape[0])]
    wc = (WordCloud(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
        .add("",data, word_size_range=[20, 50], shape='pentagon')
        .set_global_opts(title_opts=opts.TitleOpts(title=''))
        .render('{}词云.html'.format(word))
        )
    
## 设置headers和cookie，数据爬取
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0',
'Connection': 'keep-alive'}
cookies ='v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
cookie = {}
for line in cookies.split(';'):
    name, value = cookies.strip().split('=', 1)
    cookie[name] = value


resou = pd.DataFrame(columns=['date','title','searchCount','rank'])
resou_date = getBetweenDay('2019/01/01','2019/07/12')
for i in resou_date:
    print(i)
    url= 'https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date={}'.format(str(i))
    html = requests.get(url=url, cookies=cookie, headers=header).content
    data = json.loads(html.decode('utf-8'))
    for j in range(100):
        resou = resou.append({'date':i,'title':data[j]['keyword'],
                                'searchCount':data[j]['searchCount'],'rank':j+1},ignore_index=True)
 

## 按天统计    
resou = resou.apply(get_words_list,axis=1)
resou.to_excel('热搜数据.xlsx')
resou_dt = resou.groupby('date',as_index=False).agg({'searchCount':['mean']})
resou_dt.columns = ['date','avg_count']


## 绘制日历图
from pyecharts import options as opts
from pyecharts.charts import Calendar,Pie
from pyecharts import GraphicShapeOpts
from pyecharts.globals import SymbolType
from pyecharts.charts import Page, WordCloud,TreeMap
data = [
        [resou_dt['date'][i], resou_dt['avg_count'][i]]
        for i in range(resou_dt.shape[0])
    ]



calendar = (
        Calendar(init_opts=opts.InitOpts(width='1800px',height='1500px'))
        .add("", data,calendar_opts=opts.CalendarOpts(range_=['2019-01-01', '2019-07-12']))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2019每日热搜平均指数",pos_left='15%'),
            visualmap_opts=opts.VisualMapOpts(
                max_=3600000,
                min_=0,
                orient="horizontal",
                is_piecewise=False,
                pos_top="230px",
                pos_left="100px",
                pos_right="10px"
            )
            )
        .render('日期热力图.html')     
     )


## 词频统计
resou_word = dataframe_explode(resou,'words_list')
resou_word_stat = resou_word.groupby(['words_list'],as_index=False).agg({'title':['count']}) 
resou_word_stat.columns = ['word','num']
resou_word_stat.to_excel('词频统计.xlsx')

func = pd.read_excel('名词.xlsx')
love = pd.read_excel('婚恋.xlsx')
person = pd.read_excel('人物.xlsx')
resou_word_func = pd.merge(resou_word_stat,func,how='inner',on='word')
resou_word_love = pd.merge(resou_word_stat,love,how='inner',on='word')
resou_word_person = pd.merge(resou_word_stat,person,how='inner',on='word')


resou_word_func = resou_word_func.sort_values('count',ascending=False).reset_index()
words = [(resou_word_func['word'][i],resou_word_func['num'][i]) for i in range(resou_word_func.shape[0])]
pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
        .add("", words)
        .set_global_opts(title_opts=opts.TitleOpts(title="微博常用词出现次数",pos_left='center'),
                         legend_opts=opts.LegendOpts(is_show=False))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}",font_size=16),)
        .render('热搜词饼图.html')
    )
        
        
resou_word_love = resou_word_love.sort_values('count',ascending=False).reset_index()
words = [(resou_word_love['word'][i],resou_word_love['num'][i]) for i in range(resou_word_love.shape[0])]
pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
        .add("", words)
        .set_global_opts(title_opts=opts.TitleOpts(title="微博婚恋类词语出现次数",pos_left='center'),
                         legend_opts=opts.LegendOpts(is_show=False))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}",font_size=16),)
        .render('婚恋类热搜词饼图.html')
    )
        
        
resou_word_person = resou_word_person.sort_values('num',ascending=False).reset_index()        
words = [{'"value": {}, "name": {}"'.format(str(resou_word_person['num'][i]),
          resou_word_person['name'][i])} for i in range(resou_word_person.shape[0])]

tree = (
        TreeMap(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
        .add("", words,pos_left=0,pos_right=0,pos_top=50,pos_bottom=50)
        .set_global_opts(title_opts=opts.TitleOpts(title="热搜明星出现次数排名",pos_left='center'),
                         legend_opts=opts.LegendOpts(is_show=False))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}\n\n {c}",font_size=17,
                                                   color='black',position='inside',font_weight='bolder'))
        .render('排序.html')
    )
       