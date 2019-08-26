import pandas as pd
import jieba, re
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
data = pd.read_csv('test_datasets_finally.csv',delimiter='#')  # 读取Excel转为dabaframe
df = pd.DataFrame(data)
print('去掉空值前有{}行'.format(df.shape[0]))  # 获得一共有多少行
file1 = df.loc[:,'describe'].dropna(how='any')  # 去掉空值
print('去掉空值后有{}行'.format(file1.shape[0]))  # 获得一共有多少行
print(file1.head())
text1 = ''.join(i for i in file1)  # 把所有字符串连接成一个长文本
responsibility = re.sub(re.compile('，|；|\.|、|。'), '', text1)  # 去掉逗号等符号
wordlist1 = " ".join(jieba.cut(responsibility, cut_all=True))  # 分析岗位职责
# wordlist1=" ".join(jieba.cut(requirement,cut_all=True))#分析岗位要求
font_path = r'C:\Windows\Fonts\simkai.ttf'
stopwords = list(STOPWORDS) + ['数据', '分析', '负责', '相关', '公司', '进行', '工作','岗位',
'岗位职责','上学','互联网','以上','以上学历','任职','要求'] +\
 ['数据分析','以上学历','优先','计算','经验','学历','上学','熟练','使用']#分析岗位要求
#bgimg=imread(r'1.png')#设置背景图片
wc = WordCloud(font_path=font_path,  # 设置字体
               background_color="black",  # 背景颜色
               max_words=1000,  # 词云显示的最大词数
               stopwords=stopwords,  # 设置停用词
               max_font_size=300,  # 字体最大值
               #mask=bgimg,  # 设置背景图片
               random_state=42,  # 设置有多少种随机生成状态，即有多少种配色
               width=1200, height=860,
               margin=4,  # 设置图片默认的大小,margin为词语边缘距离
               ).generate(str(wordlist1))
#image_colors = ImageColorGenerator(bgimg)  # 根据图片生成词云颜色
plt.imshow(wc)
plt.axis("off")
plt.savefig("./job_pic/examples1.jpg")  # 必须在plt.show之前，不是图片空白
plt.show()
