import hashlib
import socket
import redis
import urllib
import sys
from functools import wraps
import datetime
import os
import requests
from lxml import etree
from fake_useragent import UserAgent
from urllib.parse import quote, urlencode
import time
import string
import socket
socket.setdefaulttimeout(6)


def con_redis():
    # 连接池
    pool = redis.ConnectionPool(
        host="123.56.153.183", port=6379, max_connections=1024)
    conn = redis.Redis(connection_pool=pool)
    return conn


def download(url, filename, callback):
    """
    封装了 urlretrieve()的自定义函数，递归调用urlretrieve(),当下载失败时，重新下载，三次下载失败结束
    download file from internet
    :param url: path to download from
    :param savepath: path to save files
    :return: None
    """

    count = 1
    try:
        urllib.request.urlretrieve(url, filename, callback)
    except socket.timeout:
        while count <= 2:
            try:
                urllib.request.urlretrieve(url, filename, callback)
                break
            except socket.timeout:
                err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                print(err_info)
                count += 1
    if count > 2:
        print("downloading picture fialed!")

    # try:
    #     urllib.request.urlretrieve(url, filename, callback)
    # # except urllib.ContentTooShortError:
    # #     print('Network conditions is not good.Reloading.')
    # #     download(url, filename, callback, header)
    # except Exception as e:
    #     print(e)
    #     print('Network conditions is not good.\nReloading.....')
        # download(url, filename, callback)


def download2(url, filename, callback):
    try:
        res = requests.get(url, timeout=10)
        with open(filename, 'ab') as file:  # 保存到本地的文件名
            file.write(res.content)
            file.flush()
    except socket.timeout:
        print('timeouut')


# 下载进度
def callback(num, consumed_bytes, total_bytes):
    """
    显示下载文件的进度
    :param @num:目前为此传递的数据块数量
    :param @consumed_bytes:每个数据块的大小，单位是byte,字节
    :param @total_bytes:远程文件的大小
    :return: None
    """
    # if a3:
    rate = int(100 * (float(num * consumed_bytes) / float(total_bytes)))
    print('\r{0}% '.format(rate), end='')
    sys.stdout.flush()


def cost(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print('花费', start - end, 's')
        return res

    return wrapper


def hash_str_to_md5(str: string):
    content = hashlib.md5(str.encode("utf-8")).hexdigest()
    return content
