import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = 'SimHei'## 设置中文显示
plt.rcParams['axes.unicode_minus'] = False

data=pd.read_csv('test_datasets_finally.csv',delimiter='#',header=0)
df=pd.DataFrame(data)
print(df.shape)

#### 1. 城市与薪资
area=df.loc[:,'area'].value_counts()[:30]
#area=pd.DataFrame(area)
print(area.shape)
print(area.head())
area2=area.values.tolist()
area=area.reset_index()
area1=area.loc[:,'index'].tolist()
print('地区',area1)
print('数量',area2)
p=plt.figure(figsize=(15,12))## 设置画布
p.add_subplot(2,1,1)
plt.bar(range(len(area2)),area2)## 绘制散点图
plt.xticks(range(len(area1)),area1,rotation=45)
plt.xlabel('公司地点')## 添加横轴标签
plt.ylabel('工作数量）')## 添加y轴名称
plt.title('工作地点数量直方图')## 添加图表标题

p.add_subplot(2,1,2)
df['avg_salary']=(df.low_salary+df.high_salary)/2
area=df.groupby(by='area')['avg_salary'].mean()
print(area.head())
area=area.reset_index()
area=area.sort_index(by = 'avg_salary',ascending=False)[:30]
print(area)
y=area['avg_salary'].tolist()
x=area['area'].to_list()
plt.bar(range(len(y)),y)## 绘制散点图
plt.xticks(range(len(x)),x,rotation=45)
plt.xlabel('公司类型')## 添加横轴标签
plt.ylabel('平均薪资（K）')## 添加y轴名称
plt.title('工作地点对应薪资直方图')## 添加图表标题
plt.savefig('./job_company/大数据工作地点对应薪资直方图.jpg')
plt.show()



##  2.公司类型与薪资关系
df['avg_salary']=(df.low_salary+df.high_salary)/2
print(df.avg_salary)##平均工资
print(df.loc[:,'companytype'].nunique())#地区数
company=df.loc[:,'companytype'].value_counts()
print(company)
num=company.values.tolist()[:-2]
companytype=company.index.to_list()[:-2]
p=plt.figure(figsize=(12,10))## 设置画布
ax1=p.add_subplot(2,1,1)
plt.bar(range(9),num)## 绘制散点图
plt.xticks(range(10),companytype,rotation=45)
plt.xlabel('公司类型')## 添加横轴标签
plt.ylabel('数量')## 添加y轴名称
plt.title('大数据公司类型图')## 添加图表标题
plt.savefig('./job_company/大数据公司类型图直方图.jpg')

ax2=p.add_subplot(2,1,2)
a=df.groupby(by='companytype')['avg_salary'].mean()[1:]
y=a.values.tolist()
x=a.index.to_list()
print(a.head())
print(num)
print(companytype)
ax2=p.add_subplot(2,1,2)
plt.bar(range(len(y)),y)## 绘制散点图
plt.xticks(range(10),x,rotation=45)
plt.xlabel('公司类型')## 添加横轴标签
plt.ylabel('平均薪资（K）')## 添加y轴名称
plt.title('大数据各公司类型图对应薪资')## 添加图表标题
plt.savefig('./job_company/大数据各公司类型图对应薪资直方图.jpg')
plt.show()

salary=df.loc[:,'low_salary'].value_counts()[:25]
print(salary)
low_salary_y=salary.values.tolist()
print(len(low_salary_y))
low_salary_x=salary.index.to_list()

p=plt.figure(figsize=(15,10))## 设置画布
ax1=p.add_subplot(2,1,1)
plt.bar(range(14),low_salary_y)## 绘制散点图
plt.xticks(range(14),low_salary_x,rotation=45)
plt.xlabel('万/月')## 添加横轴标签
plt.ylabel('薪资数量')## 添加y轴名称
plt.title('大数据低薪资直方图')## 添加图表标题
#plt.savefig('./job_company/大数据低薪资直方图.jpg')

salary=df.loc[:,'high_salary'].value_counts()[:30]
high_salary_y=salary.values.tolist()
print(len(high_salary_y))
high_salary_x=salary.index.to_list()
ax2=p.add_subplot(2,1,2)
plt.bar(range(len(high_salary_y)),high_salary_y)## 绘制散点图
plt.xticks(range(len(high_salary_y)),high_salary_x,rotation=45)
plt.xlabel('万/月')## 添加横轴标签
plt.ylabel('薪资数量')## 添加y轴名称
plt.title('大数据高薪资直方图')## 添加图表标题
plt.savefig('./job_company/大数据高低薪资直方图.jpg')
plt.show()




plt.figure(figsize=(6,6))## 将画布设定为正方形，则绘制的饼图是正圆
explode = [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]## 设定各项离心n个半径
plt.pie(num,explode=explode,labels=companytype,autopct='%1.1f%%')## 绘制饼图
plt.title('大数据公司类型图')
plt.legend(loc="upper right",fontsize=10,bbox_to_anchor=(1.1,1.05),borderaxespad=0.3)
plt.savefig('./job_company/大数据公司类型图饼图.jpg')
plt.show()

print(df.loc[:,'education'].nunique())#地区数
education=df.loc[:,'education'].value_counts()
print(education)
num=education.values.tolist()
education=education.index.to_list()
res=[]
for one in education:
    if u'人' not in one and u'education' not in one:
        res.append(one)
print(res)
education=df.loc[:,'education'].value_counts()
df1=education.reset_index()
print(df1.head())
new_df=df1.loc[df1['index'].isin(res)]
print(new_df)
num=new_df['education'].values.tolist()
education=new_df['index'].values.tolist()
print(num)
print(education)
plt.figure(figsize=(6,6))## 将画布设定为正方形，则绘制的饼图是正圆
explode = [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]## 设定各项离心n个半径
plt.pie(num,explode=explode,labels=education,autopct='%1.1f%%')## 绘制饼图
plt.title('大数据公司学历要求图')
plt.legend(loc="upper right",fontsize=10,bbox_to_anchor=(1.1,1.05),borderaxespad=0.3)
plt.savefig('./job_company/大数据公司学历要求饼图.jpg')
plt.show()


workyear=df.loc[:,'workyear'].value_counts()
print(workyear)
num2=workyear.values.tolist()
workyear=workyear.index.to_list()
plt.figure(figsize=(6,6))## 将画布设定为正方形，则绘制的饼图是正圆
explode = [0.01,0.01,0.01,0.01,0.01,0.01,0.01]## 设定各项离心n个半径
plt.pie(num2,explode=explode,labels=workyear,autopct='%1.1f%%')## 绘制饼图
plt.title('大数据各公司工作经验图')
plt.legend(loc="upper right",fontsize=10,bbox_to_anchor=(1.1,1.05),borderaxespad=0.3)
plt.savefig('./job_company/大数据各公司工作经验图饼图.jpg')
plt.show()

plt.figure(figsize=(6,5))## 设置画布
plt.bar(range(7),num2)## 绘制散点图
plt.xticks(range(7),workyear,rotation=25)
plt.xlabel('工作经验')## 添加横轴标签
plt.ylabel('数量')## 添加y轴名称
plt.title('大数据各公司工作经验图')## 添加图表标题
plt.savefig('./job_company/大数据各公司工作经验图饼图.jpg')
plt.show()




