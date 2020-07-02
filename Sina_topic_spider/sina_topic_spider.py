import re
import os
import csv
import json
import time
import random

import requests

# 每次请求中最小的since_id，下次请求使用，新浪分页机制
min_since_id = ''
# 生成Session对象，用于保存Cookie
s = requests.Session()
# 新浪话题数据保存文件
CSV_FILE_PATH = 'sina_topic.csv'


def login_sina():
    """
    登录新浪
    :return:
    """
    # 登录URL
    login_url = 'https://passport.weibo.cn/sso/login'
    # 请求头
    headers = {'user-agent': 'Mozilla/5.0',
               'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F'}
    # 传递用户名和密码
    data = {'username': '你的账号',
            'password': '你的密码',
            'savestate': 1,
            'entry': 'mweibo',
            'mainpageflag': 1}
    try:
        r = s.post(login_url, headers=headers, data=data)
        r.raise_for_status()
    except:
        print('登录请求失败')
        return 0
    # 打印请求结果
    print(json.loads(r.text)['msg'])
    return 1


def spider_topic():
    """
    爬取新浪话题
    新浪微博分页机制：根据时间分页，每一条微博都有一个since_id，时间越大的since_id越大
    所以在请求时将since_id传入，则会加载对应话题下比此since_id小的微博，然后又重新获取最小since_id
    将最小since_id传入，依次请求，这样便实现分页
    :return:
    """
    # 1、构造请求
    global min_since_id
    topic_url = 'https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&containerid=1008087a8941058aaf4df5147042ce104568da_-_feed'
    if min_since_id:
        topic_url = topic_url + '&since_id=' + min_since_id
    kv = {'user-agent': 'Mozilla/5.0',
          'Referer': 'https://m.weibo.cn/p/1008087a8941058aaf4df5147042ce104568da/super_index?jumpfrom=weibocom'}
    try:
        r = s.get(url=topic_url, headers=kv)
        r.raise_for_status()
    except:
        print('爬取失败')
        return
    # 2、解析数据
    r_json = json.loads(r.text)
    cards = r_json['data']['cards']
    # 2.1、第一次请求cards包含微博和头部信息，以后请求返回只有微博信息
    card_group = cards[2]['card_group'] if len(cards) > 1 else cards[0]['card_group']
    for card in card_group:
        # 创建保存数据的列表，最后将它写入csv文件
        sina_columns = []
        mblog = card['mblog']
        # 2.2、解析用户信息
        user = mblog['user']
        # 爬取用户信息，微博有反扒机制，频率太快就请求就返回418
        try:
            basic_infos = spider_user_info(user['id'])
            #print(basic_infos)
        except:
            print('用户信息爬取失败！id=%s' % user['id'])
            continue
        # 把用户信息放入列表
        sina_columns.append(user['id'])
        sina_columns.extend(basic_infos)
        # 2.3、解析微博内容
        r_since_id = mblog['id']
        # 过滤html标签，留下内容
        sina_text = re.compile(r'<[^>]+>', re.S).sub(' ', mblog['text'])
        # 除去无用开头信息
        sina_text = sina_text.replace('周杰伦超话', '').strip()
        # 将微博内容放入列表
        sina_columns.append(r_since_id)
        sina_columns.append(sina_text)
        print(sina_columns)
        # 检验列表中信息是否完整
        # sina_columns数据格式：['用户id', '用户名', '性别', '地区', '生日', '微博id', '微博内容']
        if len(sina_columns) < 7:
            print('------上一条数据内容不完整-------')
            continue

        # 3、保存数据
        save_columns_to_csv(sina_columns)

        # 4、获得最小since_id，下次请求使用
        if min_since_id:
            min_since_id = r_since_id if min_since_id > r_since_id else min_since_id
        else:
            min_since_id = r_since_id

        # 5、爬取用户信息不能太频繁，所以设置一个时间间隔
        time.sleep(random.randint(3, 6))


def spider_user_info(uid) -> list:
    """
    爬取用户信息（需要登录），并将基本信息解析成字典返回
    :return: ['用户名', '性别', '地区', '生日']
    """
    user_info_url = 'https://weibo.cn/%s/info' % uid
    print(user_info_url)
    kv = {'user-agent': 'Mozilla/5.0'}
    try:
        r = s.get(url=user_info_url, headers=kv)
        r.raise_for_status()
        #print('登录成功')
    except:
        print('爬取用户信息失败')

    # 使用正则提取基本信息
    basic_info_html = re.findall('<div class="tip">基本信息</div>.*?<div class="c">(.*?)</div>', r.text)
    # 提取：用户名、性别、地区、生日 这些基本信息
    basic_infos = get_basic_info_list(basic_info_html)
    return basic_infos


def get_basic_info_list(basic_info_html) -> list:
    """
    将html解析提取需要的字段
    :param basic_info_html:
    :return: ['用户名', '性别', '地区', '生日']
    """
    basic_infos = []
    basic_info_kvs = basic_info_html[0].split('<br/>')
    print(basic_info_kvs)
    for basic_info_kv in basic_info_kvs:
        if basic_info_kv.startswith('昵称'):
            basic_infos.append(basic_info_kv.split(':')[1])
        elif basic_info_kv.startswith('性别'):
            basic_infos.append(basic_info_kv.split(':')[1])
        elif basic_info_kv.startswith('地区'):
            area = basic_info_kv.split(':')[1]
            # 如果地区是其他的话，就添加空
            if '其他' in area or '海外' in area:
                basic_infos.append('')
                continue
            # 浙江 杭州，这里只要省
            if ' ' in area:
                area = area.split(' ')[0]
            basic_infos.append(area)
        elif basic_info_kv.startswith('生日'):
            try:
                birthday = basic_info_kv.split(':')[1]
                # 19xx 年和20xx 带年份的才有效，只有月日或者星座的数据无效
                if birthday.startswith('19') or birthday.startswith('20'):
                    # 只要前三位，如198、199、200分别表示80后、90后和00后，方便后面数据分析
                    basic_infos.append(birthday[:3])
                else:
                    basic_infos.append('')
            except:
                if len(basic_infos) < 4:
                    basic_infos.append('')
        else:
            pass
    # 有些用户的生日是没有的，所以直接添加一个空字符
    if len(basic_infos) < 4:
        basic_infos.append('')
    return basic_infos


def save_columns_to_csv(columns, encoding='utf-8'):
    """
    将数据保存到csv中
    数据格式为：'用户id', '用户名', '性别', '地区', '生日', '微博id', '微博内容'
    :param columns: ['用户id', '用户名', '性别', '地区', '生日', '微博id', '微博内容']
    :param encoding:
    :return:
    """
    with open(CSV_FILE_PATH, 'a', encoding=encoding,newline="") as csvfile:
        csv_write = csv.writer(csvfile)
        csv_write.writerow(columns)


def patch_spider_topic():
    # 爬取前先登录，登录失败则不爬取
    if not login_sina():
        return
    # 写入数据前先清空之前的数据
    if os.path.exists(CSV_FILE_PATH):
        os.remove(CSV_FILE_PATH)
    # 批量爬取
    for i in range(100):
        print('第%d页' % (i + 1))
        spider_topic()


if __name__ == '__main__':
    patch_spider_topic()
