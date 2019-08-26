from selenium import webdriver
from lxml import etree
import time
import csv
def get_info(url):
    chrome_driver=r"D:\Python\Anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
    driver=webdriver.Chrome(executable_path=chrome_driver)
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(10)
    iframe=driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)
    html=etree.HTML(driver.page_source)
    infos=html.xpath('//div[@class="srchsongst"]/div')
    for info in infos:
        song_id=info.xpath('div[2]/div/div/a/@href')[0].split('=')[-1]
        song=info.xpath('div[2]/div/div/a/b/text()')[0]
        singer1=info.xpath('div[4]/div/a')[0]
        singer=singer1.xpath('string(.)')
        album=info.xpath('div[5]/div/a/@title')[0]
        print(song_id,song,singer,album)
        writer.writerow([song_id,song,singer,album])
if __name__=='__main__':
    fp=open('music.csv','w',newline='',encoding='utf-8')
    writer=csv.writer(fp)
    writer.writerow(['song_id','song','singer','album'])
    url='https://music.163.com/#/search/m/?s=%E8%AE%B8%E5%B5%A9&type=1'
    get_info(url)