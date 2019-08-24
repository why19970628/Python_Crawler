import os
import jieba
import pickle
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Funnel
from wordcloud import WordCloud


'''柱状图(2维)'''
def drawBar(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	bar = Bar(title, title_pos='center')
	#bar.use_theme('vintage')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	bar.add('', attrs, values, xaxis_rotate=15, yaxis_rotate=30)
	bar.render(os.path.join(savepath, '%s.html' % title))


'''饼图'''
def drawPie(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	pie = Pie(title, title_pos='center')
	#pie.use_theme('westeros')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	pie.add('', attrs, values, is_label_show=True,
			legend_orient="vertical", #标签成列
			legend_pos="left",# #标签在左
			radius=[30, 75],
			rosetype="area" #宽度属性随值大小变化
	)
	pie.render(os.path.join(savepath, '%s.html' % title))


'''漏斗图'''
def drawFunnel(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	funnel = Funnel(title, title_pos='center')
	#funnel.use_theme('chalk')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	funnel.add("", attrs, values, is_label_show=True,
			   label_pos="inside",#显示标签在图像中
			   label_text_color="#fff",
			   funnel_gap=5,
			   legend_pos="left",
			   legend_orient="vertical" #标签成列
			   )
	funnel.render(os.path.join(savepath, '%s.html' % title))


'''统计词频'''
def statistics(texts, stopwords):
	words_dict = {}
	for text in texts:
		temp = jieba.cut(text)
		for t in temp:
			if t in stopwords or t == 'unknow':
				continue
			if t in words_dict.keys():
				words_dict[t] += 1
			else:
				words_dict[t] = 1
	return words_dict


'''词云'''
def drawWordCloud(words, title, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	wc = WordCloud( background_color='white', max_words=2000, width=1920, height=1080, margin=5)
	wc.generate_from_frequencies(words)
	wc.to_file(os.path.join(savepath, title+'.png'))



if __name__ == '__main__':
	with open('python_61.pkl', 'rb') as f:
		data = pickle.load(f)
	# 价格分布
	results = {}
	prices = []
	price_max = ['', 0]
	for key, value in data.items():
		price = value[1]
		if price_max[1] < price:
			price_max = [key, price]
		prices.append(price)
	results['小于50元'] = sum(i < 50 for i in prices)
	results['50-100元'] = sum((i < 100 and i >= 50) for i in prices)
	results['100-200元'] = sum((i < 200 and i >= 100) for i in prices)
	results['200-300元'] = sum((i < 300 and i >= 200) for i in prices)
	results['300-400元'] = sum((i < 400 and i >= 300) for i in prices)
	results['400元以上'] = sum(i >= 400 for i in prices)
	drawPie('python相关图书的价格分布', results)
	print('价格最高的图书为: %s, 目前单价为: %f' % (price_max[0], price_max[1]))
	# 评分分布
	results = {}
	stars = []
	for key, value in data.items():
		star = value[3] if value[3] > 0 else '暂无评分'
		stars.append(str(star))
	for each in sorted(set(stars)):
		results[each] = stars.count(each)
	drawBar('python相关图书评分分布', results)
	# 评论数量
	results = {}
	comments_num = []
	top6 = {}
	for key, value in data.items():
		num = int(value[-1])
		comments_num.append(num)
		top6[key.split('【')[0].split('（')[0].split('(')[0].split(' ')[0].split('：')[0]] = num
	results['0评论'] = sum(i == 0 for i in comments_num)
	results['0-100评论'] = sum((i > 0 and i <= 100) for i in comments_num)
	results['100-1000评论'] = sum((i > 100 and i <= 1000) for i in comments_num)
	results['1000-5000评论'] = sum((i > 1000 and i <= 5000) for i in comments_num)
	results['5000评论以上'] = sum(i > 5000 for i in comments_num)
	drawFunnel('python相关图书评论数量分布', results)
	top6 = dict(sorted(top6.items(), key=lambda item: item[1])[-6:])
	drawBar('python相关图书评论数量TOP6', top6)
	# 词云
	stopwords = open('./stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
	texts = [j[2] for i, j in data.items()]
	words_dict = statistics(texts, stopwords)
	drawWordCloud(words_dict, 'python相关图书简介词云', savepath='./results')