# coding = utf-8
import requests ,pymysql ,json
import time
from jsonpath import jsonpath
from multiprocessing.dummy import Pool

def database():
    coon = pymysql.connect(
        host='localhost', user='root', passwd='root',
        port=3306, db='data', charset='utf8'
    )
    cur = coon.cursor()  # 建立游标
    return cur, coon

Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
}
class gkcx(object):
    def __init__(self):
        self.pool = Pool()
    def get_data(self):
        for i in range(4, 145): # 145
            page = i
            print("正在下载第%s页数据" % i)
            self.start_time = time.time()
            url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_dual_class=&keyword=&page=%s&province_id=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&type=&uri=apigkcx/api/school/hotlists' % i
            res = requests.get(url, headers=Hostreferer)
            res=res.text
            data=json.loads(res)
            num=len(data["data"]["item"])
            school_ids=jsonpath(data, '$.data.item..school_id')
            school_names = jsonpath(data, '$.data.item[*].name')
            print(school_names)
            print(school_ids)
            print('有',num,'个数据')

            for i in range(0,len(school_ids)):
                school_id = school_ids[i]
                print(school_id)
                school_name = school_names[i]
                try:
                    special_name_url = 'https://static-data.eol.cn/www/2.0/school/%s/pc_special.json' % school_id # 专业名称
                    res = requests.get(special_name_url, headers=Hostreferer)
                    res = res.text
                    data = json.loads(res)
                    special_names = jsonpath(data, '$.data..special_name')
                    special_ids = jsonpath(data, '$.data..id')
                    # print(special_names)
                    # print(special_ids)
                except:
                    print('解析',school_id,special_names,'失败')
                    pass
                # 爬取在河北省的理科历年分数线
                score_url ='https://api.eol.cn/gkcx/api/?access_token=&local_province_id=13&local_type_id=1&page=1&school_id=%s&signsafe=&size=10&uri=apidata/api/gk/score/province&year=' %school_id
                # print(score_url)
                res = requests.get(score_url, headers=Hostreferer)
                res = res.text
                data = json.loads(res)
                score_list = jsonpath(data, '$..data.item..min]')
                try:
                    min_2019_score1=score_list[0]
                except:
                    min_2019_score1 = '无数据'
                try:
                    min_2018_score1=score_list[1]
                except:
                    min_2018_score1 = '无数据'
                try:
                    min_2017_score1=score_list[2]
                except:
                    min_2017_score1 ="无数据"
                try:
                    min_2016_score1 = score_list[3]
                except:
                    min_2016_score1 = "无数据"
                try:
                    min_2015_score1 = score_list[4]
                except:
                    min_2015_score1 = "无数据"
                # print(min_2019_score1,min_2018_score1,min_2017_score1,min_2016_score1,min_2015_score1)

                # 文科
                score_url = 'https://api.eol.cn/gkcx/api/?access_token=&local_province_id=13&local_type_id=2&page=1&school_id=%s&signsafe=&size=10&uri=apidata/api/gk/score/province&year=' % school_id
                # print(score_url)
                res = requests.get(score_url, headers=Hostreferer)
                res = res.text
                data = json.loads(res)
                score_list = jsonpath(data, '$..data.item..min]')
                try:
                    min_2019_score2 = score_list[0]
                except:
                    min_2019_score2 = '无数据'
                try:
                    min_2018_score2 = score_list[1]
                except:
                    min_2018_score2 = '无数据'
                try:
                    min_2017_score2 = score_list[2]
                except:
                    min_2017_score2 = "无数据"
                try:
                    min_2016_score2 = score_list[3]
                except:
                    min_2016_score2 = "无数据"
                try:
                    min_2015_score2 = score_list[4]
                except:
                    min_2015_score2 = "无数据"
                # print(min_2019_score2, min_2018_score2, min_2017_score2, min_2016_score2, min_2015_score2)


                ## 历年批次
                pc_url='https://api.eol.cn/gkcx/api/?access_token=&local_province_id=13&local_type_id=1&page=1&school_id=%s&signsafe=&size=10&uri=apidata/api/gk/score/province&year=' %school_id
                # print('批次url:',pc_url)
                res = requests.get(pc_url, headers=Hostreferer)
                res = res.text
                data = json.loads(res)
                score_list = jsonpath(data, '$.data.item..local_batch_name')
                try:
                    pici_2019 = score_list[0]
                except:
                    pici_2019= '无数据'
                try:
                    pici_2018 = score_list[1]
                except:
                    pici_2018= '无数据'
                try:
                    pici_2017 = score_list[2]
                except:
                    pici_2017 = "无数据"
                try:
                    pici_2016 = score_list[3]
                except:
                    pici_2016 = "无数据"
                try:
                    pici_2015 = score_list[4]
                except:
                    pici_2015 = "无数据"
                # print(pici_2019,pici_2018,pici_2017,pici_2016,pici_2015)

                special_class=[] #专业课list
                # special_class_id = []
                contents = []
                try:
                    for special_id ,special_name in zip(special_ids[:5],special_names[:5]): #遍历专业 id
                        special_url='https://static-data.eol.cn/www/2.0/school/%s/special/%s.json' %(school_id,special_id)
                        # print(special_url)
                        res = requests.get(special_url, headers=Hostreferer)
                        res = res.text
                        data = json.loads(res)
                        try:
                            content = jsonpath(data, '$.data..content')[0]
                        except:
                            content = '专业暂无数据'
                        # print(special_id,special_name,content)
                        special_class.append(special_name)
                        # special_class_id.append(str(special_id))
                        contents.append(content)
                        while len(special_class) < 5:
                            special_class.append("暂无招生专业")
                        while len(contents) < 5:
                            contents.append("专业暂无数据")
                except:
                    special_class=["暂无专业名","暂无专业名","暂无专业名","暂无专业名","暂无专业名"]
                    contents = ['专业暂无数据','专业暂无数据','专业暂无数据','专业暂无数据','专业暂无数据']

                #招生计划 理科
                try:
                    zhaosheng_url = 'https://api.eol.cn/gkcx/api/?access_token=&local_batch_id=7&local_province_id=13&local_type_id=1&page=1&school_id=%s&signsafe=&size=10&uri=apidata/api/gk/plan/special&year=2019' %school_id
                    # print('#招生计划:',zhaosheng_url)
                    res = requests.get(zhaosheng_url, headers=Hostreferer)
                    res = res.text
                    data = json.loads(res)
                    special_name_ = jsonpath(data, '$.data..spname')[:5]
                    require_num =  jsonpath(data, '$.data..num')[:5]
                    while len(special_name) < 5:
                        special_name.append("暂无招生数据")
                    while len(require_num) < 5:
                        require_num.append("暂无招生人数")
                except:
                    special_name_ =['-','-','-','-','-']
                    require_num=[0,0,0,0,0]
                ## 文科
                try:
                    zhaosheng_url = 'https://api.eol.cn/gkcx/api/?access_token=&local_batch_id=7&local_province_id=13&local_type_id=2&page=1&school_id=%s&signsafe=&size=10&uri=apidata/api/gk/plan/special&year=2019' % school_id
                    # print('#招生计划:', zhaosheng_url)
                    res = requests.get(zhaosheng_url, headers=Hostreferer)
                    res = res.text
                    data = json.loads(res)
                    special_name_1 = jsonpath(data, '$.data..spname')[:5]
                    require_num2 = jsonpath(data, '$.data..num')[:5]
                    while len(special_name_1)<5:
                        special_name_1.append("暂无招生数据")
                    while len(require_num2)<5:
                        require_num2.append("暂无招生人数")
                except:
                    special_name_1 = ['-', '-', '-', '-', '-']
                    require_num2 = [0, 0, 0, 0, 0]
                cur, coon = database()
                data = [page,str(school_id), school_name,
                        min_2019_score1,min_2018_score1,min_2017_score1,min_2016_score1,min_2015_score1,
                        min_2019_score2,min_2018_score2,min_2017_score2,min_2016_score2,min_2015_score2,
                        pici_2019,pici_2018,pici_2017,pici_2016,pici_2015,
                        special_class[0],special_class[1],special_class[2],special_class[3],special_class[4],
                        contents[0],contents[1],contents[2],contents[3],contents[4],
                        special_name_[0],special_name_[1],special_name_[2],special_name_[3],special_name_[4],
                        str(require_num[0]),str(require_num[1]),str(require_num[2]),str(require_num[3]),str(require_num[4]),
                        special_name_1[0],special_name_1[1],special_name_1[2],special_name_1[3],special_name_1[4],
                        str(require_num2[0]),str(require_num2[1]),str(require_num2[2]),str(require_num2[3]),str(require_num2[4])]
                sql = "replace into school2(page,school_id,school_name," \
                      "min_2019_score1,min_2018_score1,min_2017_score1,min_2016_score1,min_2015_score1," \
                      "min_2019_score2,min_2018_score2,min_2017_score2,min_2016_score2,min_2015_score2" \
                      ",pici_2019,pici_2018,pici_2017,pici_2016,pici_2015" \
                      ",special_name1,special_name2,special_name3,special_name4,special_name5," \
                      "content1,content2,content3,content4,content5," \
                      "special_name_1,special_name_2,special_name_3,special_name_4,special_name_5," \
                      "require_num_1,require_num_2,require_num_3,require_num_4,require_num_5," \
                      "special_name_21,special_name_22,special_name_23,special_name_24,special_name_25," \
                      "require_num_21,require_num_22,require_num_23,require_num_24,require_num_25) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],data[10],
                    data[11], data[12], data[13], data[14],data[15], data[16], data[17], data[18], data[19], data[20],
                    data[21], data[22], data[23], data[24],data[25],data[26], data[27], data[28], data[29], data[30]
                    , data[31], data[32], data[33], data[34], data[35],data[36],data[37], data[38], data[39], data[40]
                    , data[41], data[42], data[43], data[44], data[45], data[46],data[47])
                cur.execute(sql)
                coon.commit()
                print(school_name,"插入成功")
                # # except:
                #     print('提取信息失败')
                #     special_name = '暂无'
                #     content= '暂无'
            self.end_time = time.time()
            print('~~~~~~~~~~~~总共花了{}s'.format(self.end_time - self.start_time))
            time.sleep(10)

    def run(self):
        for i in range(5):
            self.pool.apply_async(self.get_data())

    while True:
        time.sleep(0.001)

if __name__ == '__main__':
    run=gkcx()
    run.get_data()