import requests
import json
import re
import csv
from collections import defaultdict
import jieba
from wordcloud import WordCloud as wd  # 词云
from PIL import Image  # 打开图片，用于词云背景层
import numpy as np  # 转换图片，用于词云背景层
import matplotlib.pyplot as plt  # 绘图
from matplotlib.font_manager import FontProperties  # 中文显示

font = FontProperties(fname=r"C:\Windows\Fonts\simkai.ttf", size=14)  # 设置中文字体

data = []
restaurants = []
foodtype = []


def Getdata(page):  # 爬虫
    print('正在爬取第{}页'.format(page/24))
    url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=ww30b9kh3zmq&latitude=35.295722&limit=24&longitude=113.933798&offset='+str(page)+'&terminal=web'
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
               "cookie": "你的COOKIE"}
    html = requests.get(url, headers=headers)
    content = re.findall(r'"flavors":.*?,"next_business_time"', html.text)  # 用正则获取包含数据的那部分
    print(content)

    for con in content:
        #print(con)
        jsonstring = "{" + con.replace(',"next_business_time"', "}")  # 完善格式，使其成为准确的json格式
        #print(jsonstring)
        jsonobj = json.loads(jsonstring)
        restaurant_id = jsonobj["id"]
        restaurant_name = jsonobj["name"].encode("gbk", "ignore").decode("gbk")
        print(restaurant_name)
        flavors = jsonobj["flavors"]
        restaurant_type = []
        for f in flavors:  # 有些flavors中只有一个值，有些有2个，所以要for循环
            restaurant_type.append(f["name"])
        restaurants.append(restaurant_name)  # 用于后面词云图
        foodtype.append(restaurant_type)  # 用于后面条形图
        data.append([restaurant_id, restaurant_name, restaurant_type])
    with open("elemedata.csv", "w", newline="") as f:  # 保存数据到本地
        writer = csv.writer(f)
        writer.writerow(["restaurant_id", "restaurant_name", "restaurant_type"])
        for d in data:
            writer.writerow(d)

    return restaurants, foodtype  # 返回值应用到下面2个函数


def Eleme_wordcloud(restaurants):  # 词云图
    jieba.load_userdict("fooddic.txt")
    text = ""
    for i in restaurants:
        #print(i)
        name = re.sub(r'（.*', "", i)
        #print(name)
        name = re.sub(r'\(.*', "", name)

        text = text + " " + name

    fenci = jieba.lcut(text)

    wordfrequency = defaultdict(int)
    for word in fenci:
        if word != " ":
            wordfrequency[word] += 1  # 词频统计
    #print('词频',wordfrequency)

    img = Image.open("1.png")  # 打开图片
    myimg = np.array(img)  # 转换图片

    path = "C:\Windows\Fonts\simkai.ttf"
    wordcloud = wd(width=1000, height=860, margin=2, font_path=path, background_color="white", max_font_size=100,
                   mask=myimg).fit_words(wordfrequency)  # 根据词频字典生成词云
    plt.imshow(wordcloud)
    plt.axis('off')  # 不显示坐标轴
    plt.savefig('eleme_wordcloud.png', dpi=300)
    plt.clf()  # 清除当前 figure 的所有axes，但是不关闭这个 window，所以能继续复用于其他的 plot。否则会影响下面的绘图


def Eleme_bar(foodtype):  # 条形图
    # foodtype的格式：[['盖浇饭', '简餐'],['川湘菜', '简餐'],['日韩料理']]
    wordfrequency2 = defaultdict(int)
    foodtypes = []  # 放总的类型，有重复项
    types = []  # 放词频统计后的类型，无重复项
    numbers = []  # 放词频统计后的词频
    for f in foodtype:
        for t in f:
            foodtypes.append(t)  # 把每个词汇总到列表中

    for type in foodtypes:
        wordfrequency2[type] += 1  # 用字典进行词频统计
    print(wordfrequency2)
    wordfrequency2 = sorted(wordfrequency2.items(),key=lambda x:x[1],reverse=True)  # 根据词频降序排序
    print('sorted',wordfrequency2)
    for key in wordfrequency2:
        #print(key[0],key[1])
        types.append(key[0])
        numbers.append(key[1])
    plt.bar(range(len(types)), numbers)
    plt.xticks(range(len(types)), types, fontproperties=font, fontsize=5, rotation=90)
    plt.savefig('eleme_bar.png', dpi=300)
    plt.show()
    plt.clf()


if __name__ == '__main__':
    for p in range(0,7):
        page = p * 24
        restaurants, foodtype = Getdata(page)
    Eleme_wordcloud(restaurants)
    Eleme_bar(foodtype)