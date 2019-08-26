import pandas as pd
data=pd.read_csv('test_datasets_finally.csv',delimiter='#',header=0)
df=pd.DataFrame(data)
print(df.shape)
print(df.index)
print(df.loc[:,'area'].nunique())#地区数
area=df.loc[:,'area'].value_counts()
print(area.shape)
print(area.head())
print(area.index)
area2=area.values.tolist()
area=area.reset_index()
print(area.head())
area1=area.loc[:,'index'].tolist()
print('地区',area1)
print('数量',area2)

from pyecharts import Bar
from pyecharts import Geo
from pyecharts import Map
map = Map("大数据工作分布图", "data from 51job",title_color="#404a59", title_pos="center")
map.add("", area1,area2 , maptype='china',is_visualmap=True,visual_text_color='#000',is_label_show=True)
map.render("./job_pic/大数据工作城市分布.html")
map.render(path='snapshot.png')
#map.render(path='snapshot.pdf')

#effectScatter  heatmap
geo = Geo("大数据工作分布热力图", "data from 51job", title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
geo.add("大数据工作分布热力图", area1, area2, visual_range=[0, 35], type='heatmap',visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=False)
geo.render('./job_pic/大数据工作分布热力图.html')

geo = Geo("大数据工作分布城市评分", "data from 51job", title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
# type="effectScatter", is_random=True, effect_scale=5  使点具有发散性
geo.add("空气质量评分", area1, area2,maptype='china', type="effectScatter", is_random=True, effect_scale=5, visual_range=[0, 5],visual_text_color="#fff", symbol_size=10, is_visualmap=True, is_roam=False)
geo.render("./job_pic/大数据工作分布城市评分.html")


#from pyecharts.charts import Geo
#map = Map("全国地图示例" )
#map.add("", area, maptype='china' ,visual_text_color="#fff",symbol_size=10, is_visualmap=True)
#map.render("全国大数据工作城市.html")
#map