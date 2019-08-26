import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei'## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False

data=pd.read_csv('test_datasets_finally.csv',delimiter='#',header=0)
df=pd.DataFrame(data)
print(df.shape)
df['avg_salary']=(df.low_salary+df.high_salary)/2
#print(df.avg_salary)


####城市与薪资
#area=df.loc[:,'area'].value_counts()[:30]
##area=pd.DataFrame(area)
#print(area.shape)
#print(area.head())
#area2=area.values.tolist()
#area=area.reset_index()
#area1=area.loc[:,'index'].tolist()
#print('地区',area1)
#print('数量',area2)
#p=plt.figure(figsize=(12,10))## 设置画布
#p.add_subplot(2,1,1)
#plt.bar(range(len(area2)),area2)## 绘制散点图
#plt.xticks(range(len(area1)),area1,rotation=35)
#plt.ylabel('工作数量）')## 添加y轴名称
#plt.title('工作地点数量直方图')## 添加图表标题
#
#p.add_subplot(2,1,2)
#area=df.groupby(by='area')['avg_salary'].mean()
#print(area.head())
#area=area.reset_index()
#area=area.sort_index(by = 'avg_salary',ascending=False)[:30]
#print(area)
#y=area['avg_salary'].tolist()
#x=area['area'].to_list()
#plt.bar(range(len(y)),y)## 绘制散点图
#plt.xticks(range(len(x)),x,rotation=45)
#plt.xlabel('工作地点')## 添加横轴标签
#plt.ylabel('平均薪资（K）')## 添加y轴名称
#plt.title('工作地点对应薪资直方图')## 添加图表标题
#plt.savefig('./job_company/大数据工作地点对应薪资直方图.jpg')
#plt.show()


####学历经验与薪资
p=plt.figure(figsize=(10,8))## 设置画布
ax2=p.add_subplot(2,1,2)
education=df.groupby(by='education')['avg_salary'].mean()
#print(education)

num=education.values.tolist()
education_list=education.index.to_list()
res=[]
for one in education_list:
    if u'人' not in one and u'education' not in one:
        res.append(one)
print(res)
#education=df.loc[:,'education'].value_counts()
df1=education.reset_index()
print(df1)
new_df=df1.loc[df1['education'].isin(res)]
new_df=new_df.sort_index(by = 'avg_salary',ascending=False)
print(new_df)
educations=new_df['education'].values.tolist()
avg_salary=new_df['avg_salary'].values.tolist()
print(avg_salary)
print(educations)
#avg_salary=df.loc[:,'avg_salary'].value_counts()

#学历对应薪资直方图
ax2=p.add_subplot(2,1,1)
plt.bar(range(len(avg_salary)),avg_salary)## 绘制散点图
plt.xticks(range(len(educations)),educations)
plt.xlabel('学历')## 添加横轴标签
plt.ylabel('平均薪资（K）')## 添加y轴名称
plt.title('大数据学历对应薪资')## 添加图表标题
plt.savefig('./job_company/大数据学历对应薪资直方图.jpg')

#经验对应薪资直方图
ax2=p.add_subplot(2,1,2)
a=df.groupby(by='workyear')['avg_salary'].mean()
a=a.reset_index()
a=a.sort_index(by = 'avg_salary',ascending=False)
y=a['avg_salary'].tolist()
x=a['workyear'].to_list()
print(a.head())
ax2=p.add_subplot(2,1,2)
plt.bar(range(len(y)),y)## 绘制散点图
plt.xticks(range(len(x)),x)
plt.xlabel('工作经验')## 添加横轴标签
plt.ylabel('平均薪资（K）')## 添加y轴名称
plt.title('大数据经验对应薪资')## 添加图表标题
plt.savefig('./job_company/大数据学历与经验对应薪资直方图.jpg')
plt.show()

#import pandas as pd
#data=pd.read_csv('test_datasets.csv',delimiter='#',header=0)
#df=pd.DataFrame(data)
#print(df.shape)
#print(df.columns)
#print(df.head())
#df=df.loc[:,['salary','area']]
#print(df)
#data=pd.read_csv('test_datasets_finally.csv',delimiter='#',header=0)
#df=pd.DataFrame(data)
#print(df.shape)
#df=df.loc[:,['salary','low_salary','high_salary','area']]
#print(df)
#print(df.loc[:,'education'].nunique())#地区数
#education=df.loc[:,'education'].value_counts()
#print(education)
#num=education.values.tolist()
#education=education.index.to_list()
#res=[]
#for one in education:
#    if u'人' not in one and u'education' not in one:
#        res.append(one)
#print(res)
#education=df.loc[:,'education'].value_counts()
#df=education.reset_index()
#print(df)
#new_df=df.loc[df['index'].isin(res)]
#print(new_df)
#num=new_df['education'].values.tolist()
#education=new_df['index'].values.tolist()
#print(num)
#print(education)
#