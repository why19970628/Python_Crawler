from  urllib import  request
import urllib
import random
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
import re
def get_ip():
    fr=open('ip.txt','r')
    ips=fr.readlines()
    new=[]
    for line in ips:
        temp=line.strip()
        new.append(temp)
    ip=random.choice(new)
    return ip
    print(ip)
proxy =get_ip()
proxy_handler = ProxyHandler({
'http': 'http://' + proxy,
'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
import  threading
class One(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        try:
            for i in range(1,5,2):
                pageurl='http://www.58pic.com/piccate/3-0-0-p'+str(i)+'.html'
                data =urllib.request.urlopen(pageurl).read().decode('utf-8','ignore')
                pat='class="card-trait".*?src="(.*?).jpg!'
                image_url=re.compile(pat).findall(data)
                print('url个数',len(image_url))
                for j in range(0,len(image_url)):
                    try:
                        this_list=image_url[j]
                        this_url='https:'+this_list+'.jpg!w1024_0'
                        file='D:/软件（学习）/Python/Test/chapter6/qiantu.photo/'+str(i)+str(j)+'.jpg'
                        urllib.request.urlretrieve(this_url,file)
                        print('第'+str(i)+'页第'+str(j)+'个图片成功')
                    except urllib.error.URLError as e:
                        print(e.reason)

        except URLError as e:
            print(e.reason)


class Two(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            for i in range(2, 5, 2):
                pageurl = 'http://www.58pic.com/piccate/3-0-0-p'+str(i)+'.html'
                data = urllib.request.urlopen(pageurl).read().decode('utf-8', 'ignore')
                pat = 'class="card-trait".*?src="(.*?).jpg!'
                image_url = re.compile(pat).findall(data)
                for j in range(0, len(image_url)):
                    try:
                        this_list = image_url[j]
                        this_url = 'https:'+this_list + '.jpg!w1024_0'
                        file = 'D:/软件（学习）/Python/Test/chapter6/qiantu.photo/' + str(i) + str(j) + '.jpg'
                        urllib.request.urlretrieve(this_url, file)
                        print('第' + str(i) + '页第' + str(j) + '个图片成功')
                    except urllib.error.URLError as e:
                        print(e.reason)

        except URLError as e:
            print(e.reason)
one=One()
one.start()
two=Two()
two.start()