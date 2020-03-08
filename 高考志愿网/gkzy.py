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
        print('777')
        # 30
        for i in range(1, 145): # 145
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
            addresss=jsonpath(data, '$.data.item..address')
            level_names=jsonpath(data, '$.data.item..level_name')
            school_types=jsonpath(data, '$.data.item..school_type')
            school_ranks=jsonpath(data, '$.data.item..rank')
            banxue_types=jsonpath(data, '$.data.item..type_name')

            print('有',num,'个数据')
            try:
                for i in range((len(school_ids))):
                    school_id = school_ids[i]
                    school_name = school_names[i]
                    address = addresss[i]
                    level_name = level_names[i]  # 办学类型
                    school_type = school_types[i]  # 高校类型
                    school_rank = school_ranks[i]  # 学校排名
                    banxue_type = banxue_types[i]  # 院校类型
                    try:
                        zhaoban_url = 'https://static-data.eol.cn/www/school/%s/info.json' % school_id
                        res = requests.get(zhaoban_url, headers=Hostreferer)
                        res = res.text
                        data = json.loads(res)
                        zhaoban_url = data["site"]
                        school_url = data["school_site"]
                    except:
                        zhaoban_url = '无'
                        school_url = '无'

                    score_list = []
                    for i in range(2015, 2020):
                        school_api = 'https://api.eol.cn/gkcx/api/?access_token=&local_province_id=11&local_type_id=1&school_id=%s&signsafe=&uri=apidata/api/gk/score/province&year=%s' % (
                        str(school_id), str(i))
                        res = requests.get(school_api, headers=Hostreferer)
                        res = res.text
                        data = json.loads(res)
                        try:
                            school_batch = data["data"]["item"][0]["local_batch_name"]  # 层次
                        except:
                            school_batch = '无'
                        try:
                            score = data["data"]["item"][0]["min"]
                        except:
                            score = '--'
                        score_list.append(str(score))

                    cur, coon = database()
                    data = [str(school_id), school_name, address, level_name, str(school_type), str(school_rank),
                            banxue_type, school_batch, school_url, zhaoban_url] + score_list
                    print(data)
                    sql = "replace into school(school_id,school_name,address,level_name,school_type,school_rank,banxue_type,school_batch,school_url,zhaoban_url,score_2015,score_2016,score_2017,score_2018,score_2019) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                        data[10],
                        data[11], data[12], data[13], data[14])

                    cur.execute(sql)
                    coon.commit()
            except:
                print('~~~~~~~~第',i ,'个查找失败')
            self.end_time = time.time()
            print('~~~~~~~~~~~~总共花了{}s'.format(self.end_time - self.start_time))
            time.sleep(5)

    # def _callback(self, temp):
    #     self.pool.apply_async(self.get_data(), callback=self._callback)
    #
    # def run(self):
    #     for i in range(5):
    #         self.pool.apply_async(self.get_data(), callback=self._callback)

    # while True:
    #     time.sleep(0.001)
if __name__ == '__main__':
    run=gkcx()
    run.get_data()