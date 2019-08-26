from  urllib import  request
import urllib
import random
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
import json
import jieba.analyse
import pymysql
from wordcloud import WordCloud
from scipy.misc import imread

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
def get_comment():
    try:
        headers = ('User-Agent',' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
        start = 0
        step = 20
        for i in range(start, 21, step):
            url='https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='+str(i)
            req =urllib.request.Request(url)
            response = opener.open(req).read().decode('utf-8')
            response_dict = json.loads(response)
            subjects = response_dict['subjects']
            #print(subjects)
            for subject in subjects:
                movie_id = subject['id']
                movie_title = subject['title']
                #movie_rate = subject['rate']
                #movie_cover = subject['cover']
                #movie_url = subject['url']
                print(movie_id)
                print(movie_title)


                # 链接 MySQL 的豆瓣数据库
                host = 'localhost'
                user = 'root'
                pwd = ''
                database = 'douban'
                db = pymysql.connect(host,user,pwd,database)
                cursor = db.cursor()  # 获取一个邮标，增删减除

                from bs4 import BeautifulSoup
                import re
                start1 = 0
                step1 = 20
                for a in range(start1, 41, step1):  #评论
                    url1 = 'https://movie.douban.com/subject/'+str(movie_id)+'/comments?start=' + str(
                        a) + 'sort=new_score&status=P'
                    res =opener.open(url1).read().decode('utf-8')
                    bs = BeautifulSoup(res, 'lxml')
                    pat1 = '<span class="short">(.*?)</span>'
                    comments= re.compile(pat1).findall(str(bs))
                    comment_list=''
                    for short_comment in comments:
                        comment_list=str(short_comment+'   '+comment_list)
                cursor.execute("insert ignore into short_comment2 values('%s','%s','%s')" % (movie_id,movie_title, comment_list))
                db.commit()
                        #print(comment)
    except URLError as e:
        print(e.reason)

#get_comment()
#exit()

def get_wordcloud():
    try:
        host = 'localhost'
        user = 'root'
        pwd = ''
        database = 'douban'
        db = pymysql.connect(host, user, pwd, database)
        cursor = db.cursor()  # 获取一个邮标，增删减除
        cursor.execute("select movie_name from short_comment2")
        movie_titles = cursor.fetchall()
        db.commit()

        cursor.execute("select short_comment_content from short_comment2")
        movie_comments = cursor.fetchall()
        db.commit()
        movie_comments=list(movie_comments)
        movie_titles=list(movie_titles)

        movie_comment2 = movie_comments.__str__()
        for a in range(len(movie_comments)):
            movie_title1=movie_titles[a]
            movie_comment1=movie_comments[a]
            movie_title=list(movie_title1)[0]
            movie_comment=list(movie_comment1)[0]
            words = jieba.cut(str(movie_comment), cut_all=False)
            word_list = ''
            for word in words:
                word_list = word_list + ' ' + word
            #print(word_list)
            color_mask = imread("1.png")
            wc = WordCloud(
                background_color="black",  # 背景颜色
                max_words=100,  # 显示最大词数
                font_path="D:/软件（学习）/Python/PyCharm/font/simsun.ttc",  # 使用字体
                min_font_size=15,
                max_font_size=150,
                width=400,
                height=860,
                mask=color_mask)  # 图幅宽度
            wc.generate(str(word_list))
            file = str(movie_title)
            wc.to_file('D:/软件（学习）/Python/PyCharm/kaoshi/pic/'+str(file)+".png")
    except URLError as e:
        print(e.reason)
get_wordcloud()