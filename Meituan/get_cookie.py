from selenium import webdriver
import requests
import time
import json
from lxml import etree


# 返回一个ip和对应的cookie，cookie以字符串形式返回。ip需要经过测试
def get_cookie():
    mark = 0
    while mark == 0:
        # 购买的ip获取地址
        p_url = 'XXXXXXXXXXXXX'
        r = requests.get(p_url)
        html = json.loads(r.text)
        a = html['data'][0]['ip']
        b = html['data'][0]['port']
        val = '--proxy-server=http://' + str(a) + ':' + str(b)
        val2 = 'https://' + str(a) + ':' + str(b)
        p = {'https': val2}
        print('获取IP：', p)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(val)
        driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',
                                  chrome_options=chrome_options)
        driver.set_page_load_timeout(8)  # 设置超时
        driver.set_script_timeout(8)
        url = 'https://i.meituan.com/shenzhen/'  # 美团深圳首页
        url2 = 'https://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1'  # 美食页面
        try:
            driver.get(url)
            time.sleep(2.5)
            c1 = driver.get_cookies()
            now = time.time()
            driver.get(url2)
            tt = time.time() - now
            print(tt)
            time.sleep(0.5)
            # ip速度测试，打开时间大于3S的NG
            if tt < 3:
                c = driver.get_cookies()
                driver.quit()
                print('*******************')
                print(len(c1), len(c))
                # 判断cookie是否完整，正常的长度应该是18
                if len(c) > 17:
                    mark = 1
                    # print(c)
                    x = {}
                    for line in c:
                        x[line['name']] = line['value']
                    # 将cookie合成字符串，以便添加到header中，字符串较长就分了两段处理
                    co1 = '__mta=' + x['__mta'] + '; client-id=' + x['client-id'] + '; IJSESSIONID=' + x[
                        'IJSESSIONID'] + '; iuuid=' + x[
                              'iuuid'] + '; ci=30; cityname=%E6%B7%B1%E5%9C%B3; latlng=; webp=1; _lxsdk_cuid=' + x[
                              '_lxsdk_cuid'] + '; _lxsdk=' + x['_lxsdk']
                    co2 = '; __utma=' + x['__utma'] + '; __utmc=' + x['__utmc'] + '; __utmz=' + x[
                        '__utmz'] + '; __utmb=' + x['__utmb'] + '; i_extend=' + x['i_extend'] + '; uuid=' + x[
                              'uuid'] + '; _hc.v=' + x['_hc.v'] + '; _lxsdk_s=' + x['_lxsdk_s']
                    co = co1 + co2
                    print(co)
                    return (p, co)
                else:
                    print('缺少Cookie,长度：', len(c))
            else:
                print('超时')
                driver.quit()
                time.sleep(3)
        except:
            driver.quit()
            pass

    # 解析店铺详情页面，返回店铺信息info和一个标志位mark
    # 传入参数u包含url和店铺分类，pc包含cookie和ip，m代表抓取的数量，n表示线程号，ll表示剩余店铺数量，ttt该线程抓取的总时长


def parse(u, pc, m, n, ll, ttt):
    mesg = 'Thread:' + str(n) + ' No:' + str(m) + ' Time:' + str(ttt) + ' left:' + str(ll)  # 记录当前线程爬取的信息
    url = u[0]
    cate = u[1]
    p = pc[0]
    cookie = pc[1]
    mark = 0  # 标志位，0表示抓取正常，1,2表示两种异常
    head = {'Host': 'meishi.meituan.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade - Insecure - Requests': '1',
            'Referer': 'https://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
            'Cookie': cookie
            }
    info = []  # 店铺信息存储
    try:
        r = requests.get(url, headers=head, timeout=3, proxies=p)
        r.encoding = 'utf-8'
        html = etree.HTML(r.text)
        datas = html.xpath('body/script[@crossorigin="anonymous"]')
        for data in datas:
            try:
                strs = data.text[:16]
                if strs == 'window._appState':
                    result = data.text[19:-1]
                    result = json.loads(result)
                    name = result['poiInfo']['name']
                    addr = result['poiInfo']['addr']
                    phone = result['poiInfo']['phone']
                    aveprice = result['poiInfo']['avgPrice']
                    opentime = result['poiInfo']['openInfo']
                    opentime = opentime.replace('\n', ' ')
                    avescore = result['poiInfo']['avgScore']
                    marknum = result['poiInfo']['MarkNumbers']
                    lng = result['poiInfo']['lng']
                    lat = result['poiInfo']['lat']
                    info = [name, cate, addr, phone, aveprice, opentime, avescore, marknum, lng, lat]
                    print(url)
                    print(mesg, name, cate, addr, phone, aveprice, opentime, avescore, marknum, lng, lat)
            except:
                pass
    except Exception  as e:
        print('Error  Thread:', n)  # 打印出异常的线程号
        print(e)
        s = str(e)[-22:-6]
        if s == '由于目标计算机积极拒绝，无法连接':
            print('由于目标计算机积极拒绝，无法连接', n)
            mark = 1  # 1类错误，需要更换ip
        else:
            mark = 2  # 2类错误，再抓取一次
    return (mark, info)  # 返回标志位和店铺信息

