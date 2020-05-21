import execjs
import os
import requests
from requests import exceptions
import json
import xlwt
import time


# 获取商铺信息
def get_shop_info(session, wm_latitude=22634767, wm_longitude=113834247):
    """
    :param wm_longitude: 定位的经度
    :param wm_latitude: 定位的纬度
    :param session: 保持会话的实例
    :return: 商铺列表
    """
    # header_cookie = ";".join([x + '=' + str(y) for x, y in cookie.items()])  # 请求头的Cookies拼接
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://h5.waimai.meituan.com',
        'Referer': 'https://h5.waimai.meituan.com/waimai/mindex/home',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36',
        'Cookie': "lxsdk_cuid=16915455dbec8-08db788af7a2ff-1333063-1fa400-16915455dbec8; ci=30; _ga=GA1.3.2111621561.1550840081; _gid=GA1.3.426525714.1550840081; IJSESSIONID=1oa4mjr7l5r0c1fa32alvdcpbn; iuuid=C2540F1F12DE8DEB7EFFE84661C401CBEDED6125E30E08F9BF648F828AD42BDF; cityname=%E6%B7%B1%E5%9C%B3; _lxsdk=C2540F1F12DE8DEB7EFFE84661C401CBEDED6125E30E08F9BF648F828AD42BDF; webp=1; ci3=1; _hc.v=f8c27eb3-603c-e958-93d8-63f0bfa0a746.1550840270; __utmz=74597006.1550906260.3.3.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; latlng=22.636802,113.829362,1550906262992; i_extend=C_b1Gimthomepagecategory1394H__a; openh5_uuid=C2540F1F12DE8DEB7EFFE84661C401CBEDED6125E30E08F9BF648F828AD42BDF; showTopHeader=show; _lxsdk_s=1691935afe6-838-f5a-f2%7C%7C44; _lx_utm=utm_source%3D60030; __utma=74597006.2078366826.1550840256.1550901561.1550906260.3; __utmc=74597006; wm_order_channel=mtib; __mta=51223190.1550840082094.1550840082094.1550840111070.2"
    }
    start_index = 0
    data = {
        'startIndex': start_index,  # 页数；从0开始
        'sortId': 5,  # 排序方式；0是综合排序，5是距离最近
        'multiFilterIds': '',
        'sliderSelectCode': '',
        'sliderSelectMin': '',
        'sliderSelectMax': '',
        'geoType': 2,
        'wm_latitude': wm_latitude,  # 定位坐标
        'wm_longitude': wm_longitude,
        'wm_actual_latitude': 22634767,  # 真实坐标
        'wm_actual_longitude': 113834247,
        '_token': '',
    }
    url = "https://i.waimai.meituan.com/openh5/homepage/poilist?_={}".format(execjs.eval("Date.now()"))
    print(f"当前爬取坐标({data['wm_longitude']},{data['wm_latitude']})")
    try:
        # 只爬取第四页，后续数据需要登录才能获取
        for index in range(4):
            res = session.post(url=url, headers=headers, data=data, timeout=5)

            # 返回数据成功
            if res.status_code == 200:
                shop_list = json.loads(res.text).get("data").get("shopList")
                return shop_list
            else:
                print("get_shop_info：返回数据失败，status_code非200")
            start_index += 1  # 页数加1
            time.sleep(2)

    except exceptions.ConnectionError:
            print("get_shop_info：网络连接错误")

    except exceptions.Timeout:
            print("get_shop_info：超过等待时间")


# 保存商铺信息
def save_shop_info(path, data, name='shopInfo.xls'):
    # 文件路径拼接
    filepath = os.path.join(path, name)

    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("shopInfo", cell_overwrite_ok=True)

    # Excel写入头部
    title = ['店铺ID', '店铺名称', '评分', '月销售量', '地址']
    for i in range(len(title)):
        sheet.write(0, i, title[i])

    # Excel写入数据
    dict_key = ['mtWmPoiId', 'shopName', 'wmPoiScore', 'monthSalesTip', 'address']  # 需要写入的key值
    for h in range(len(data)):
        _dict = data[h]
        for l in range(len(dict_key)):
            content = _dict.get(dict_key[l])
            sheet.write(h+1, l, content)

    # 保存Excel
    book.save(filepath)


# 获取商品信息
def get_food_info(shop_list, session):
    data_list = []
    # 遍历所有店铺
    for _dict in shop_list:
        shop_id = _dict.get("mtWmPoiId")
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://h5.waimai.meituan.com',
            'Referer': 'https://h5.waimai.meituan.com/waimai/mindex/menu?dpShopId=&mtShopId={}&source=shoplist'.format(shop_id),
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36',
            'Cookie': "lxsdk_cuid=16915455dbec8-08db788af7a2ff-1333063-1fa400-16915455dbec8; ci=30; _ga=GA1.3.2111621561.1550840081; _gid=GA1.3.426525714.1550840081; IJSESSIONID=1oa4mjr7l5r0c1fa32alvdcpbn; iuuid=C2540F1F12DE8DEB7EFFE84661C401CBEDED6125E30E08F9BF648F828AD42BDF; cityname=%E6%B7%B1%E5%9C%B3; _lxsdk=C2540F1F12DE8DEB7EFFE84661C401CBEDED6125E30E08F9BF648F828AD42BDF; webp=1; ci3=1; _hc.v=f8c27eb3-603c-e958-93d8-63f0bfa0a746.1550840270; __utmz=74597006.1550906260.3.3.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; latlng=22.636802,113.829362,1550906262992; i_extend=C_b1Gimthomepagecategory1394H__a; openh5_uuid=C2540F1F12DE8DEB7EFFE84661C401CBEDED6125E30E08F9BF648F828AD42BDF; showTopHeader=show; _lxsdk_s=1691935afe6-838-f5a-f2%7C%7C44; _lx_utm=utm_source%3D60030; __utma=74597006.2078366826.1550840256.1550901561.1550906260.3; __utmc=74597006; wm_order_channel=mtib; __mta=51223190.1550840082094.1550840082094.1550840111070.2"
        }
        data = {
            'geoType': '2',
            'mtWmPoiId': shop_id,
            'dpShopId': '-1',
            'source': 'shoplist',
            'skuId': '',
            '_token': '',
        }
        # 拼接API接口
        url = "https://i.waimai.meituan.com/openh5/poi/food?_={}".format(execjs.eval("Date.now()"))

        # 针对网络问题、请求超时、数据返回状态进行异常捕获
        try:
            response = session.post(url=url, headers=headers, data=data, timeout=5)

            # 是否返回成功
            if response.status_code == 200:
                _data = json.loads(response.text)

                # 是否返回正确数据
                if _data.get("msg") == "成功":
                    data_dict = _data.get("data")
                    data_list.append(data_dict)
            else:
                print("get_food_info：status_code非200")
        except exceptions.ConnectionError:
            print("get_food_info：网络连接错误")
        except exceptions.Timeout:
            print("get_food_info：超过等待时间")
        print("*" * 30 + "【{}】商品信息保存完毕".format(_dict.get("shopName")) + "*" * 30)
        time.sleep(2)

    return data_list


# 保存商铺信息
def save_food_info(path, data_list, name='foodInfo.xls'):
    filepath = os.path.join(path, name)
    book = xlwt.Workbook(encoding="utf-8")
    # sheet = book.add_sheet("foodInfo", cell_overwrite_ok=False)
    sheet = book.add_sheet("foodInfo", cell_overwrite_ok=True)

    # Excel写入头部
    title = ['店铺ID', '店铺名称', '商品名称', '原价格', '现价格', '月销售量', '点赞数', '规格', '商品类别']
    for i in range(len(title)):
        sheet.write(0, i, title[i])

    # Excel写入数据
    write_list = []  # 待写入Excel表格的数据;二维列表

    # 遍历所有数据列表
    for data in data_list:
        shop_id = data.get("mtWmPoiId")  # 商品ID
        shop_name = data.get("shopInfo").get("shopName")  # 商品名称
        category_list = data.get("categoryList")

        # 遍历所有分类的商品
        for category in category_list:
            category_name = category.get("categoryName")  # 商品类别
            food_list = category.get("spuList")  # 商品列表

            # 遍历获取商品属性
            for i in food_list:
                write_list.append([shop_id, shop_name, i.get("spuName"), i.get("originPrice"), i.get("currentPrice"),
                                   i.get("saleVolume"), i.get("praiseNum"), i.get("unit"), category_name])

    # 二维列表写入Excel表格
    for h in range(len(write_list)):

        # 每一列写入
        for l in range(len(write_list[h])):
            sheet.write(h+1, l, write_list[h][l])

    book.save(filepath)
    print("=" * 30 + "商品信息全部写入完毕：{}".format(name) + "=" * 30)


def main():
    s = requests.session()  # 会后续使用cookie保持会话做准备
    shop_list = get_shop_info(s)
    food_list = get_food_info(shop_list=shop_list, session=s)
    save_shop_info(path='./', data=shop_list)
    save_food_info(path='./', data_list=food_list)


if __name__ == "__main__":
    main()
