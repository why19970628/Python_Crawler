import time
import pickle
import random
import requests
from bs4 import BeautifulSoup


headers = {
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'no-cache',
	'Connection': 'keep-alive',
	'Host': 'search.dangdang.com'
}



'''解析, 提取需要的数据'''
def parseHtml(html):
	data = {}
	soup = BeautifulSoup(html, 'lxml')
	conshoplist = soup.find_all('div', {'class': 'con shoplist'})[0]
	for each in conshoplist.find_all('li'):
		# 书名
		bookname = each.find_all('a')[0].get('title').strip(' ')
		# 书图
		img_src = each.find_all('a')[0].img.get('data-original')
		if img_src is None:
			img_src = each.find_all('a')[0].img.get('src')
		img_src = img_src.strip(' ')
		# 价格
		price = float(each.find_all('p', {'class': 'price'})[0].span.text[1:])
		# 简介
		detail = each.find_all('p', {'class': 'detail'})[0].text
		# 评分
		stars = float(each.find_all('p', {'class': 'search_star_line'})[0].span.span.get('style').split(': ')[-1].strip('%;')) / 20
		# 评论数量
		num_comments = float(each.find_all('p', {'class': 'search_star_line'})[0].a.text[:-3])
		data[bookname] = [img_src, price, detail, stars, num_comments]
	return data


'''主函数'''
def main(keyword):
	url = 'http://search.dangdang.com/?key={}&act=input&page_index={}'
	results = {}
	num_page = 0
	while True:
		num_page += 1
		print('[INFO]: Start to get the data of page%d...' % num_page)
		page_url  = url.format(keyword, num_page)
		res = requests.get(page_url, headers=headers)
		if '抱歉，没有找到与“%s”相关的商品，建议适当减少筛选条件' % keyword in res.text:
			break
		page_data = parseHtml(res.text)
		results.update(page_data)
		time.sleep(random.random() + 0.5)
	with open('%s_%d.pkl' % (keyword, num_page-1), 'wb') as f:
		pickle.dump(results, f)
	return results


if __name__ == '__main__':
	main('python')