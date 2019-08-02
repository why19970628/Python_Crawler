# import urllib
from urllib import request
# import requests
# url2='http://music.163.com/song/media/outer/url?id=423776423.mp3'
# print(url2)
# urllib.request.urlretrieve(url2,'3.mp3')
# music_res = requests.get(url2)
# with open('4.mp3','wb') as f:
    # f.write(music_res.content)
# print('成功')

import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import re

headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

# 歌单的url地址
play_url = 'http://music.163.com/playlist?id=2182968685'

# 获取页面内容
s = requests.session()
response = s.get(play_url, headers=headers).content

# 使用bs4匹配出对应的歌曲名称和地址
s = BeautifulSoup(response, 'lxml')
main = s.find('ul', {'class': 'f-hide'})
pat='data-rid="(.*?)"'
singerid=re.compile(pat).findall(str(s))
id=singerid[0]
print(singerid[0])

lists = []
for music in main.find_all('a'):
    list = []
    # print('{} : {}'.format(music.text, music['href']))
    musicUrl = 'http://music.163.com/song/media/outer/url' + music['href'][5:] + '.mp3'
    musicName = music.text
    # 单首歌曲的名字和地址放在list列表中
    list.append(musicName)
    list.append(musicUrl)
    # 全部歌曲信息放在lists列表中
    lists.append(list)

print(lists)

# 下载列表中的全部歌曲，并以歌曲名命名下载后的文件，文件位置为当前文件夹
for i in lists:
    url = i[1]
    name = i[0]
    try:
        folder = os.path.exists(id)

        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(id)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print
            "---  new folder...  ---"
            print
            "---  OK  ---"

        else:
            print
            "---  There is this folder!  ---"
        print('正在下载', name)
        file="D:/软件（学习）/Python/TanZhou/百度音乐/"+id+'/'+name+".mp3"
        urllib.request.urlretrieve(url, file)
        print('下载成功')
    except:
        print('下载失败')