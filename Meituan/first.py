# coding=utf-8
import csv
import time
import requests
import json


# 区域店铺id ct_Poi cateName抓取，传入参数为区域id
def crow_id(areaid):
    id_list = []
    url = 'https://meishi.meituan.com/i/api/channel/deal/list'
    head = {'Host': 'meishi.meituan.com',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
            'Cookie': 'XXXXXXXXXXXXXX'
            }
    p = {'https': 'https://27.157.76.75:4275'}
    data = {"uuid": "09dbb48e-4aed-4683-9ce5-c14b16ae7539", "version": "8.3.3", "platform": 3, "app": "",
            "partner": 126, "riskLevel": 1, "optimusCode": 10,
            "originUrl": "http://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
            "offset": 0, "limit": 15, "cateId": 1, "lineId": 0, "stationId": 0, "areaId": areaid, "sort": "default",
            "deal_attr_23": "", "deal_attr_24": "", "deal_attr_25": "", "poi_attr_20043": "", "poi_attr_20033": ""}
    r = requests.post(url, headers=head, data=data, proxies=p)
    result = json.loads(r.text)
    totalcount = result['data']['poiList']['totalCount']  # 获取该分区店铺总数，计算出要翻的页数
    datas = result['data']['poiList']['poiInfos']
    print(len(datas), totalcount)
    for d in datas:
        d_list = ['', '', '', '']
        d_list[0] = d['name']
        d_list[1] = d['cateName']
        d_list[2] = d['poiid']
        d_list[3] = d['ctPoi']
        id_list.append(d_list)
    print('Page：1')
    # 将数据保存到本地csv
    with open('meituan_id.csv', 'a', newline='', encoding='gb18030')as f:
        write = csv.writer(f)
        for i in id_list:
            write.writerow(i)

    # 开始爬取第2页到最后一页
    offset = 0
    if totalcount > 15:
        totalcount -= 15
        while offset < totalcount:
            id_list = []
            offset += 15
            m = offset / 15 + 1
            print('Page:%d' % m)
            # 构造post请求参数，通过改变offset实现翻页
            data2 = {"uuid": "09dbb48e-4aed-4683-9ce5-c14b16ae7539", "version": "8.3.3", "platform": 3, "app": "",
                     "partner": 126, "riskLevel": 1, "optimusCode": 10,
                     "originUrl": "http://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
                     "offset": offset, "limit": 15, "cateId": 1, "lineId": 0, "stationId": 0, "areaId": areaid,
                     "sort": "default",
                     "deal_attr_23": "", "deal_attr_24": "", "deal_attr_25": "", "poi_attr_20043": "",
                     "poi_attr_20033": ""}
            try:
                r = requests.post(url, headers=head, data=data2, proxies=p)
                print(r.text)
                result = json.loads(r.text)
                datas = result['data']['poiList']['poiInfos']
                print(len(datas))
                for d in datas:
                    d_list = ['', '', '', '']
                    d_list[0] = d['name']
                    d_list[1] = d['cateName']
                    d_list[2] = d['poiid']
                    d_list[3] = d['ctPoi']
                    id_list.append(d_list)
                # 保存到本地
                with open('meituan_id.csv', 'a', newline='', encoding='gb18030')as f:
                    write = csv.writer(f)
                    for i in id_list:
                        write.writerow(i)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # 直接将html代码中区域的信息复制出来，南澳新区的数据需要处理下，它下面没有分区
    a = {"areaObj": {"28": [{"id": 28, "name": "全部", "regionName": "福田区", "count": 4022},
                            {"id": 1056, "name": "香蜜湖", "regionName": "香蜜湖", "count": 105},
                            {"id": 744, "name": "梅林", "regionName": "梅林", "count": 421},
                            {"id": 1055, "name": "上沙/下沙", "regionName": "上沙/下沙", "count": 291},
                            {"id": 2008, "name": "华强南", "regionName": "华强南", "count": 263},
                            {"id": 742, "name": "八卦岭/园岭", "regionName": "八卦岭/园岭", "count": 217},
                            {"id": 741, "name": "华强北", "regionName": "华强北", "count": 572},
                            {"id": 743, "name": "皇岗/水围", "regionName": "皇岗/水围", "count": 136},
                            {"id": 756, "name": "新城市广场", "regionName": "新城市广场", "count": 140},
                            {"id": 6595, "name": "车公庙", "regionName": "车公庙", "count": 305},
                            {"id": 6596, "name": "景田", "regionName": "景田", "count": 144},
                            {"id": 6597, "name": "新洲/石厦", "regionName": "新洲/石厦", "count": 374},
                            {"id": 6974, "name": "竹子林", "regionName": "竹子林", "count": 107},
                            {"id": 6975, "name": "市民中心", "regionName": "市民中心", "count": 39},
                            {"id": 7993, "name": "会展中心", "regionName": "会展中心", "count": 461},
                            {"id": 7994, "name": "岗厦", "regionName": "岗厦", "count": 110},
                            {"id": 7996, "name": "福田保税区", "regionName": "福田保税区", "count": 29}],
                     "29": [{"id": 29, "name": "全部", "regionName": "罗湖区", "count": 2191},
                            {"id": 6976, "name": "国贸", "regionName": "国贸", "count": 232},
                            {"id": 758, "name": "莲塘", "regionName": "莲塘", "count": 125},
                            {"id": 2009, "name": "笋岗", "regionName": "笋岗", "count": 159},
                            {"id": 748, "name": "翠竹路沿线", "regionName": "翠竹路沿线", "count": 42},
                            {"id": 745, "name": "东门", "regionName": "东门", "count": 484},
                            {"id": 746, "name": "宝安南路沿线", "regionName": "宝安南路沿线", "count": 67},
                            {"id": 757, "name": "火车站", "regionName": "火车站", "count": 96},
                            {"id": 6598, "name": "万象城", "regionName": "万象城", "count": 127},
                            {"id": 6599, "name": "喜荟城/水库", "regionName": "喜荟城/水库", "count": 99},
                            {"id": 7659, "name": "地王大厦", "regionName": "地王大厦", "count": 85},
                            {"id": 8469, "name": "黄贝岭", "regionName": "黄贝岭", "count": 136},
                            {"id": 8470, "name": "春风万佳/文锦渡", "regionName": "春风万佳/文锦渡", "count": 19},
                            {"id": 8471, "name": "布心/太白路", "regionName": "布心/太白路", "count": 154},
                            {"id": 8790, "name": "田贝/水贝", "regionName": "田贝/水贝", "count": 85},
                            {"id": 8794, "name": "银湖/泥岗", "regionName": "银湖/泥岗", "count": 37},
                            {"id": 8795, "name": "新秀/罗芳", "regionName": "新秀/罗芳", "count": 33},
                            {"id": 13080, "name": "梧桐山", "regionName": "梧桐山", "count": 34},
                            {"id": 14095, "name": "KK mall", "regionName": "KK mall", "count": 74}],
                     "30": [{"id": 30, "name": "全部", "regionName": "南山区", "count": 3905},
                            {"id": 751, "name": "南头", "regionName": "南头", "count": 325},
                            {"id": 750, "name": "华侨城", "regionName": "华侨城", "count": 126},
                            {"id": 749, "name": "蛇口", "regionName": "蛇口", "count": 9},
                            {"id": 1057, "name": "南油", "regionName": "南油", "count": 218},
                            {"id": 1058, "name": "科技园", "regionName": "科技园", "count": 460},
                            {"id": 1059, "name": "西丽", "regionName": "西丽", "count": 586},
                            {"id": 4811, "name": "南山中心区", "regionName": "南山中心区", "count": 635},
                            {"id": 6591, "name": "海岸城/保利", "regionName": "海岸城/保利", "count": 158},
                            {"id": 6592, "name": "前海", "regionName": "前海", "count": 32},
                            {"id": 6593, "name": "白石洲", "regionName": "白石洲", "count": 190},
                            {"id": 6594, "name": "欢乐海岸", "regionName": "欢乐海岸", "count": 22},
                            {"id": 7597, "name": "太古城", "regionName": "太古城", "count": 57},
                            {"id": 7599, "name": "花园城", "regionName": "花园城", "count": 42},
                            {"id": 13109, "name": "海上世界", "regionName": "海上世界", "count": 225},
                            {"id": 23117, "name": "世界之窗", "regionName": "世界之窗", "count": 97},
                            {"id": 25152, "name": "南山京基百纳", "regionName": "南山京基百纳", "count": 22},
                            {"id": 36635, "name": "深圳湾", "regionName": "深圳湾", "count": 17}],
                     "31": [{"id": 31, "name": "全部", "regionName": "盐田区", "count": 407},
                            {"id": 754, "name": "大小梅沙", "regionName": "大小梅沙", "count": 36},
                            {"id": 755, "name": "沙头角", "regionName": "沙头角", "count": 118},
                            {"id": 8789, "name": "东部华侨城", "regionName": "东部华侨城", "count": 11},
                            {"id": 8796, "name": "盐田海鲜食街", "regionName": "盐田海鲜食街", "count": 22},
                            {"id": 15349, "name": "壹海城", "regionName": "壹海城", "count": 51},
                            {"id": 38055, "name": "溪涌", "regionName": "溪涌", "count": ""}],
                     "32": [{"id": 32, "name": "全部", "regionName": "宝安区", "count": 6071},
                            {"id": 6587, "name": "西乡", "regionName": "西乡", "count": 15},
                            {"id": 6586, "name": "新安", "regionName": "新安", "count": 413},
                            {"id": 6585, "name": "石岩", "regionName": "石岩", "count": 466},
                            {"id": 752, "name": "宝安中心区", "regionName": "宝安中心区", "count": 458},
                            {"id": 4653, "name": "港隆城", "regionName": "港隆城", "count": 137},
                            {"id": 6588, "name": "沙井", "regionName": "沙井", "count": 824},
                            {"id": 6589, "name": "福永", "regionName": "福永", "count": 631},
                            {"id": 7684, "name": "松岗", "regionName": "松岗", "count": 435},
                            {"id": 7685, "name": "公明", "regionName": "公明", "count": 433},
                            {"id": 7719, "name": "海雅缤纷城", "regionName": "海雅缤纷城", "count": 125},
                            {"id": 7735, "name": "固戍", "regionName": "固戍", "count": 237},
                            {"id": 8006, "name": "桃源居", "regionName": "桃源居", "count": 25},
                            {"id": 14404, "name": "时代城", "regionName": "时代城", "count": 2},
                            {"id": 17088, "name": "罗田/燕川", "regionName": "罗田/燕川", "count": 45},
                            {"id": 17089, "name": "西田", "regionName": "西田", "count": 29},
                            {"id": 17091, "name": "圳美", "regionName": "圳美", "count": 32},
                            {"id": 17092, "name": "田寮/长圳", "regionName": "田寮/长圳", "count": 3},
                            {"id": 23524, "name": "沙井京基百纳", "regionName": "沙井京基百纳", "count": 98},
                            {"id": 27275, "name": "宝立方", "regionName": "宝立方", "count": 125},
                            {"id": 36634, "name": "宝安机场", "regionName": "宝安机场", "count": 244},
                            {"id": 37084, "name": "光明新区", "regionName": "光明新区", "count": 1}],
                     "33": [{"id": 33, "name": "全部", "regionName": "龙岗区", "count": 5193},
                            {"id": 753, "name": "罗岗/求水山", "regionName": "罗岗/求水山", "count": 145},
                            {"id": 6600, "name": "五和/民营市场", "regionName": "五和/民营市场", "count": 250},
                            {"id": 6601, "name": "平湖", "regionName": "平湖", "count": 356},
                            {"id": 7656, "name": "横岗", "regionName": "横岗", "count": 568},
                            {"id": 7658, "name": "南澳", "regionName": "南澳", "count": 32},
                            {"id": 7663, "name": "南联", "regionName": "南联", "count": 311},
                            {"id": 7664, "name": "坪地", "regionName": "坪地", "count": 131},
                            {"id": 8472, "name": "大运", "regionName": "大运", "count": 186},
                            {"id": 9013, "name": "李朗聚星商城", "regionName": "李朗聚星商城", "count": 63},
                            {"id": 13335, "name": "较场尾/大鹏所城", "regionName": "较场尾/大鹏所城", "count": 152},
                            {"id": 13358, "name": "水头", "regionName": "水头", "count": 20},
                            {"id": 13359, "name": "东涌", "regionName": "东涌", "count": 2},
                            {"id": 13361, "name": "万科广场/世贸", "regionName": "万科广场/世贸", "count": 107},
                            {"id": 13412, "name": "华南城/奥特莱斯", "regionName": "华南城/奥特莱斯", "count": 191},
                            {"id": 18069, "name": "大芬/南岭", "regionName": "大芬/南岭", "count": 359},
                            {"id": 18228, "name": "双龙", "regionName": "双龙", "count": 316},
                            {"id": 19456, "name": "慢城/三联", "regionName": "慢城/三联", "count": 111},
                            {"id": 19457, "name": "布吉街/东站/天虹", "regionName": "布吉街/东站/天虹", "count": 404},
                            {"id": 26297, "name": "天虹/坂田/杨美", "regionName": "天虹/坂田/杨美", "count": 344},
                            {"id": 26298, "name": "岗头/万科/雪象", "regionName": "岗头/万科/雪象", "count": 199},
                            {"id": 35919, "name": "华为坂田基地", "regionName": "华为坂田基地", "count": 9},
                            {"id": 36519, "name": "杨梅坑/桔钓沙", "regionName": "杨梅坑/桔钓沙", "count": 39},
                            {"id": 36520, "name": "葵涌", "regionName": "葵涌", "count": 37},
                            {"id": 36530, "name": "官湖", "regionName": "官湖", "count": 9},
                            {"id": 36531, "name": "西涌", "regionName": "西涌", "count": 49},
                            {"id": 36636, "name": "坪山高铁站", "regionName": "坪山高铁站", "count": 41},
                            {"id": 37501, "name": "龙岗中心城", "regionName": "龙岗中心城", "count": 365}],
                     "9553": [{"id": 9553, "name": "全部", "regionName": "龙华区", "count": 3080},
                              {"id": 1061, "name": "龙华", "regionName": "龙华", "count": 958},
                              {"id": 6584, "name": "民治", "regionName": "民治", "count": 164},
                              {"id": 7721, "name": "观澜", "regionName": "观澜", "count": 433},
                              {"id": 7722, "name": "大浪", "regionName": "大浪", "count": 398},
                              {"id": 9326, "name": "梅林关", "regionName": "梅林关", "count": 125},
                              {"id": 9327, "name": "锦绣江南", "regionName": "锦绣江南", "count": 33},
                              {"id": 36633, "name": "深圳北站", "regionName": "深圳北站", "count": 190},
                              {"id": 37723, "name": "龙华新区", "regionName": "龙华新区", "count": 14}],
                     "23420": [{"id": 23420, "name": "全部", "regionName": "坪山区", "count": 393},
                               {"id": 6602, "name": "坪山", "regionName": "坪山", "count": 232},
                               {"id": 23429, "name": "坑梓/竹坑", "regionName": "坑梓/竹坑", "count": 128},
                               {"id": 9535, "name": "南澳大鹏新区", "regionName": "南澳大鹏新区", "count": 91}]

                     }}

    datas = a['areaObj']
    b = datas.values()
    area_list = []
    for data in b:
        for d in data[1:]:
            area_list.append(d)  # 将每个区域信息保存到列表，元素是字典
    l = 0
    old = time.time()
    for i in area_list:
        l += 1
        print('开始抓取第%d个区域：' % l, i['regionName'], '店铺总数：', i['count'])
        try:
            crow_id(i['id'])
            now = time.time() - old
            print(i['name'], '抓取完成！', '时间:%d' % now)
        except Exception as e:
            print(e)
