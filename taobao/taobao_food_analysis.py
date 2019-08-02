# 项目目的：
#
# 对商品标题进行文本分析以及词云可视化
# 商品价格分布情况分析
# 商品的销量分布情况分析
# 商品价格对销量的影响分析
# 商品价格对销售额的影响分析
# 不同省份或城市的商品数量分布
#
# 项目步骤：
#
# 数据采集模块：利用Python爬虫爬取淘宝网商品数据
# 数据预处理模块：对商品数据进行清洗和处理
# 数据分析模块：jieba分词、wordcloud可视化、数据分析及可视化
#
# 项目环境：
#
# 　　系统环境：win10
# 64
# 位
#
# 　　工具：pycharm，chrome
# devTools，Anaconda



import pandas as pd
import numpy as np
import pymysql
import re
coon = pymysql.connect(
    host='localhost', user='root', passwd='',
    port=3306, db='taobao', charset='utf8'
    # port必须写int类型
    # charset必须写utf8，不能写utf-8
)
cur = coon.cursor()  # 建立游标
sql='select * from taobao_food'
df=pd.read_sql(sql=sql,con=coon)
#print(df.values)
df=pd.DataFrame(df)
df=df.drop('id',axis=1)
print(pd.isnull(df).values.any())


print('去重之前的形状',df.shape)
df=df.drop_duplicates(keep='first')
print('去重之后的形状',df.shape)
print(df.head())
#print(df.shop.value_counts)



def get_buy_num(buy_num):
    if u'万' in buy_num:  # 针对1-2万/月或者10-20万/年的情况，包含-
        buy_num=float(buy_num.replace("万",''))*10000
        #print(buy_num)
    else:
        buy_num=float(buy_num)
    return buy_num

from sklearn.svm import LinearSVC



df['place'] = df['place'].replace('','未知')#fillna("['未知']")
datasets = pd.DataFrame()
for index, row in df.iterrows():
    #print(row["place"])
    row["place"] = row["place"][:2]
    row["buy_num"]=get_buy_num(row["buy_num"][:-3].replace('+',''))
    #print(row["place"])

df.to_csv('taobao_food.csv',encoding="utf_8_sig",index_label=True)

#不同省份或城市的商品购买数量分布
print('place前五行:\n',df['place'].head())

from pyecharts import Bar
from pyecharts import Geo
from pyecharts import Map
## 商品所在城市分布情况
address=df['place'].value_counts()
b=address.values.tolist()[1:]
a=address.index.tolist()[1:]
print('place值前五行\n')
print(a,len(a))
print(b,len(b))
## 可以看出，大部分还是在沿海城市发货
geo = Geo("商品所在城市分布情况", "data from taobao_food", title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
# type="effectScatter", is_random=True, effect_scale=5  使点具有发散性
geo.add("城市数量", a,b , type="effectScatter",maptype='china', is_random=True, effect_scale=5, visual_range=[0, 350],visual_text_color="#fff", symbol_size=10, is_visualmap=True, is_roam=False)
geo.render("商品所在城市分布情况.html")





a=df['buy_num'].sort_values(ascending=False)
b=df.loc[df['buy_num'].sort_values(ascending=False).index,'place']
c=df.loc[df['buy_num'].sort_values(ascending=False).index,'shop']
frames = [a,c,b]
data=pd.concat(frames,axis=1)
print('销售排名商店与所在城市信息分布\n',data)

#地区销售总量信息分布
buy_num_sum=df.groupby(['place'])['buy_num'].sum().sort_values(ascending=False)
print('地区销售总量信息分布\n',buy_num_sum)
brougt=buy_num_sum.values.tolist()
address=buy_num_sum.index.tolist()
print(brougt)
print(address)

map = Map("地区销售总量信息分布", "data from 51job",title_color="#404a59", title_pos="left")
map.add("销售总量", address,brougt , maptype='china',visual_range=[0, 300000],is_visualmap=True,visual_text_color='#000',is_label_show=True,is_map_symbol_show=False)
map.render("地区销售总量信息分布图.html")






#所有店铺信息统计
print(df['shop'].value_counts()[:20])
shop=df['shop'].value_counts()[:20]
a=shop.index.to_list()
print(a)
b=shop.values
print(b)
# 主题
#
# 除了默认的白色底色和dark之外，还支持安装扩展包
#
# pip install  echarts-themes-pypkg
#  echarts-themes-pypkg 提供了 vintage, macarons, infographic, shine 和 roma 主题
from pyecharts import Bar
bar = Bar('所有店铺信息统计','直方图',width = 1200, height = 800)
#bar.use_theme('dark')
kwargs = dict(
    name = '店铺数量',
    x_axis = a,
    y_axis = b,
    #bar_category_gap = 20,
    xaxis_name='店铺',
    xaxis_name_pos= "start",
    xaxis_name_size='50',
    xaxis_name_gap= 10,  # x轴名称与轴线的距离 默认=25
    yaxis_name='数量',
    interval='0',#显示完全标签，1为隔一个显示
    xaxis_rotate='30',
    is_label_show=True,#显示数量

)
bar.add(**kwargs)
bar.render('直方图.html')



#购买人数与商铺的排名信息:
#print(df['buy_num'].sort_values(ascending=False))
#print(df.loc[df['buy_num'].sort_values(ascending=False).index,'shop'])
a=df['buy_num'].sort_values(ascending=False)
b=df.loc[df['buy_num'].sort_values(ascending=False).index,'shop']
c=df.loc[df['buy_num'].sort_values(ascending=False).index,'title']
frames = [a,b,c]
data=pd.concat(frames,axis=1)
print(data)

#title生成词云
