from selenium import webdriver
import re
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
import time
from lxml import etree
from time import sleep
import random
#from pyquery import PyQuery as pq
from selenium.webdriver.support import expected_conditions as EC
chrome_driver = r"D:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
browser = webdriver.Chrome(executable_path=chrome_driver)
wait=WebDriverWait(browser,3)


def search():
    browser.get('https://www.taobao.com')
    #sleep(5)
    #input = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#q')))
    #submit=wait.until(EC.element_to_be_clickable(By.CSS_SELECTOR,"#J_TSearchForm > div.search-button"))
    browser.find_element_by_name('q').send_keys('美食')
    sleep(2)
    browser.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()  ##搜索按钮
    browser.find_element_by_xpath('//*[@class="forget-pwd J_Quick2Static"]').click() #点击密码登录
    sleep(3)
    #browser.find_element_by_name('weibo-login').click()
    browser.find_element_by_xpath('//*[@id="J_OtherLogin"]/a[1]').click() #点击微博登录
    sleep(3)
    browser.find_element_by_name('username').send_keys('微博号')
    browser.find_element_by_name('password').send_keys('微博密码')

    #a=input('请输入验证码:',)
    #browser.find_element_by_name('verifycode').send_keys(a)
    browser.find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[7]/div[1]/a').click()
    sleep(2)

    #browser.find_element_by_xpath('//*[@id="J_SearchForm"]/button').click()  ##搜索
    #sleep(3)
    total=browser.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]')
    print(total.text)
    sleep(3)
    get_products(1)
    return total.text

def database():
    coon = pymysql.connect(
        host='localhost', user='root', passwd='',
        port=3306, db='taobao', charset='utf8'
    )
    cur = coon.cursor()  # 建立游标
    return cur, coon

def get_products(page):
        price = browser.find_elements_by_xpath('//div[@class="price g_price g_price-highlight"]/strong')
        title = browser.find_elements_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div/div[2]/div[2]/a')
        place = browser.find_elements_by_xpath('//div[@class="row row-3 g-clearfix"]/div[2]')
        buy_num = browser.find_elements_by_xpath('//div[@class="row row-1 g-clearfix"]/div[2]')
        shop=browser.find_elements_by_xpath('//div[@class="shop"]/a/span[2]')
        print('第', page, '页,共有---', len(price), '个数据')

        prices = []
        for i in price:
            try:
                price1 = i.text
            except:
                price1 == None
            prices.append(price1)
        print(prices)
        titles=[]
        for i in title:
            try:
                title1 = i.text
            except:
                title1==None
            titles.append(title1)
        print(titles)

        places = []
        for i in place:
            try:
                place1 = i.text
            except:
                price1 == None
            places.append(place1)
        print(places)

        buy_nums = []
        for i in buy_num:
            try:
                buy_num1 = i.text
            except:
                buy_num1 == None
            buy_nums.append(buy_num1)
        print(buy_nums)

        shops = []
        for i in shop:
            try:
                shop1 = i.text
            except:
                shop1 == None
            shops.append(shop1)
        print(shops)
        cur,coon=database()
        for i in range(len(price)):
            try:
                shop=shops[i]
                buy_num=buy_nums[i]
                price=prices[i]
                title=titles[i]
                place=places[i]
                ss = (str(shop),str(title), str(price), str(place), str(buy_num))
                print(ss)
                sql = "insert into taobao_food(shop,title,price,place,buy_num) VALUE('%s','%s','%s','%s','%s')" % ss
                cur.execute(sql)
            except:
                pass
        coon.commit()
        print('------------------------------页数-------------------------------------')

import pymysql

def next_page(page_number):
    try:
        input=browser.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[2]/input')
        submit=browser.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[2]/span[3]')
        input.clear()
        input.send_keys(page_number)
        submit.click()
        print('第' + str(page_number) + '页正在翻------------')
        #print(browser.find_element_by_css_selector('#mainsrp-pager > div > div > div > ul > li.item.active > span'))
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products(page_number)
    except TimeoutError:
        next_page(page_number)
def main():
    total=search()
    time.sleep(random.uniform(8, 0))
    total=int(re.compile('(\d+)').search(total).group(1))
    #print(total)
    for i  in range(87,total+1):
        next_page(i)
        time.sleep(random.uniform(8, 10))

if __name__ == '__main__':
    main()
