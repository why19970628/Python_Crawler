import pandas as pd
import re
def clean_data_quchong_key():
    data=pd.read_csv('test_datasets.csv',delimiter='#',header=0)
    df=pd.DataFrame(data)
    print(df.shape)
    df=df.dropna()##去除有任意的缺失值
    print(df.shape)
    #print(df.head())
    print('去重之前形状',df.shape)
    df=df.drop_duplicates(subset='companyname')#去重
    print('去重之后形状',df.shape)
    df=df[df[r'describe'].str.contains(r'.*?数据.*?|.*?分析.*?|.*?python.*?')]#提取包含数据或者分析的岗位
    print('包含关键字',df.shape)
    #df=df.iloc[:,1]#提取包含数据或者分析的岗位
    df.to_csv('test_datasets_cleaned1.csv',sep='#')
#clean_data_quchong_key()

def get_salary(salary):
    if '-' in salary:  # 针对1-2万/月或者10-20万/年的情况，包含-
        low_salary = re.findall(re.compile('(\d*\.?\d+)'), salary)[0]
        high_salary = re.findall(re.compile('(\d?\.?\d+)'), salary)[1]
        if u'万' in salary and u'年' in salary:  # 单位统一成千/月的形式
            low_salary = float(low_salary) / 12 * 10
            high_salary = float(high_salary) / 12 * 10
        elif u'万' in salary and u'月' in salary:
            low_salary = float(low_salary) * 10
            high_salary = float(high_salary) * 10
    else:  # 针对20万以上/年和100元/天这种情况，不包含-，取最低工资，没有最高工资
        low_salary = re.findall(re.compile('(\d*\.?\d+)'), salary)[0]
        high_salary = ""
        if u'万' in salary and u'年' in salary:  # 单位统一成千/月的形式
            low_salary = float(low_salary) / 12 * 10
        elif u'万' in salary and u'月' in salary:
            low_salary = float(low_salary) * 10
        elif u'元' in salary and u'天' in salary:
            low_salary = float(low_salary) / 1000 * 21  # 每月工作日21天
    return low_salary, high_salary

def clean_data_salary():
    data = pd.read_csv('test_datasets_cleaned1.csv', delimiter='#', header=0)
    df = pd.DataFrame(data)
    datasets = pd.DataFrame()
    for index, row in df.iterrows():
        area = row["area"][:2]
        job = row["job"]
        companyname=row['companyname']
        salary = row["salary"]
        workyear = row["workyear"]
        if salary:#如果待遇这栏不为空，计算最低最高待遇
            getsalary=get_salary(salary)
            low_salary=getsalary[0]
            high_salary=getsalary[1]
        else:
            low_salary=high_salary=""
        try:
            salary = str(int(float(low_salary)) / 10) + '-' + str(int(float(high_salary)) / 10) + '万/月'
            print(salary)
            print('正在写入第{}条，工资{},最低工资是{}k,最高工资是{}k'.format(index, salary, low_salary, high_salary))
        except Exception as e:
            print(e)
            continue
        education= row["education"]
        welfare= row["welfare"]
        companytype= row["companytype"]
        companyscale = row["companyscale"]
        describe = row["describe"]
        link = row["link"]
        datalist = [
            str(area),
            str(job),
            str(companyname),
            str(education),
            str(salary),
            str(low_salary),
            str(high_salary),
            str(workyear),
            str(welfare),
            str(companytype),
            str(companyscale),
            str(describe),
            str(link)]
        series = pd.Series(datalist, index=[
            'area',
            'job',
            'companyname',
            'education',
            'salary',
            'low_salary',
            'high_salary',
            'workyear',
            'welfare',
            'companytype',
            'companyscale',
            'describe',
            'link'
        ])
        series = pd.Series(series)
        datasets = datasets.append(series, ignore_index=True)
    print(datasets)
    datasets.to_csv('test_datasets_finally.csv', mode='a+', sep='#', index=False, index_label=False, encoding='utf-8')

clean_data_salary()



