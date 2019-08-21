from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
from time import sleep
import csv
chrome_driver = r"D:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
browser = webdriver.Chrome(executable_path=chrome_driver)
wait=WebDriverWait(browser,3)
browser.get('https://map.baidu.com/search/%E6%96%B0%E4%B9%A1%E4%BA%92%E8%81%94%E7%BD%91%E5%A4%A7%E5%8E%A6%E9%83%BD%E6%9C%89%E5%93%AA%E4%BA%9B%E5%85%AC%E5%8F%B8/@12683385.160376176,4180157.68,19z?querytype=s&da_src=shareurl&wd=%E6%96%B0%E4%B9%A1%E4%BA%92%E8%81%94%E7%BD%91%E5%A4%A7%E5%8E%A6%E9%83%BD%E6%9C%89%E5%93%AA%E4%BA%9B%E5%85%AC%E5%8F%B8&c=152&src=0&pn=0&sug=0&l=19&b=(12682905.160376176,4179893.43;12683865.160376176,4180421.93)&from=webmap&biz_forward=%7B%22scaler%22:1,%22styles%22:%22pl%22%7D&device_ratio=1')
sleep(3)

def search(writer):
    for i in range(10):

        company_names    =   browser.find_elements_by_xpath('//div[@class="ml_30 mr_90"]/div[@class="row"]/span/a')
        print(len(company_names))

        company_addresses =   browser.find_elements_by_xpath('//div[@class="ml_30 mr_90"]/div[@class="row addr"]/span')
        print(len(company_addresses))


        # ipone_lists=[]
        # try:
        #     ipones=browser.find_elements_by_xpath('//div[@class="ml_30 mr_90"]/div[@class="row tel"]')#电话
        #     for i in ipones:
        #         ipone_lists.append(ipones[i])
        # except:
        #     ipone_lists.append('无')
        # if browser.find_elements_by_xpath('//div[@class="row tel"]'):
        #     company_iphones r= browser.find_elements_by_xpath('//div[@class="ml_30 mr_90"]/div[@class="row tel"]')
        #     for i in range(len(company_iphones)):
        #         ipone_lists.append(company_iphones[i].text)
        # ipone_lists.append('无')
        # print(ipone_lists)
        # print(len(ipone_lists))

        for i in range(len(company_names)):
            company_name = company_names[i].text

            company_address = company_addresses[i].text

            print(company_name, company_address)
            # ipone_list=ipone_lists[i]

            writer.writerow([company_name, company_address])

        browser.find_element_by_xpath('//div[@id="poi_page"]/p/span/a[@tid="toNextPage"]').click()
        sleep(5)


def main():
    fp = open('company.csv', 'w', newline='', encoding="utf_8_sig")
    writer = csv.writer(fp)
    writer.writerow(['公司名称', '地址', '电话'])
    search(writer)
    print('Over ！！！！')







if __name__ == '__main__':
    main()
