import time
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
import pandas as pd
from selenium import webdriver
from multiprocessing.dummy import Pool  # 导入线程池
from multiprocessing import Pool  #这样导入的Pool表示的是进程池；
from lxml import etree


class DouYuSpider(object):

    def __init__(self):
        #self.option = webdriver.ChromeOptions()
        #self.option.add_argument('--headless')
        self.chrome_driver = r"D:\Python\Anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver)
        self.url = "https://www.douyu.com/directory/all"
        # 创建一个Chrome浏览器对象

        self.housedetail=[]
        # 进行计数
        self.count = 0
        # 创建线程池 默认最大5个
        self.pool = Pool()

    # 解析数据
    def parse_data(self, data):
        # 1.转类型
        element = etree.HTML(data)
        # 2.解析

        # 主播昵称
        nick_name_list = element.xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a[1]/div[2]/div[2]/h2/text()')

        # 直播所属分类
        category_list = element.xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a[1]/div[2]/div[1]/span/text()')
        # print(category_list)

        # 主播房间名称
        room_name_list = element.xpath('//div[@class="DyListCover-info"]/h3/text()')

        # 主播房间号
        room_id_list = element.xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a[2]/@href')

        # 主播人气
        hot_list = element.xpath('//*[@id="listAll"]/section[2]/div[2]/ul/li/div/a[1]/div[2]/div[2]/span/text()')


        for nick_name, category, room_name, room_id, hot in zip(nick_name_list, category_list, room_name_list,
                                                                 room_id_list, hot_list):
            result = {}
            result['name']=nick_name.strip()
            result['con']=category.strip()
            result['room']=room_name.strip()
            result['id']=room_id.strip()
            result['hot']=hot.strip()
            print(result)
            self.housedetail.append(result)
        return self.housedetail

    # 保存数据
    def write_file(self, data):
        data = pd.DataFrame(data)
        data.to_csv('douyu2.csv')

    def execute_request_save(self):
        # 1.获取下一页的class属性的值
        # 最后的下一页的父级li标签中的 aria-disabled=true
        # 而开始的下一页的 aria-disabled=false
        res = self.driver.find_element_by_xpath('//span[text()="下一页"]/..').get_attribute('aria-disabled')

        if res == 'false':
            # 1.1点击下一页按钮　进行翻页
            next = self.driver.find_element_by_xpath('//span[text()="下一页"]')
            time.sleep(1)
            next.click()

            # 1.2js代码　滚动到最后位置
            time.sleep(1.5)
            code_js = 'window.scrollTo(0,document.body.scrollHeight)'
            self.driver.execute_script(code_js)

            # 2.获取数据
            data = self.driver.page_source

            # 3.解析数据
            result_list = self.parse_data(data)

            # 4.保存数据
            self.write_file(result_list)

    def _callback(self, temp):
        # apply_async是异步非阻塞的
        self.pool.apply_async(self.execute_request_save, callback=self._callback)

    # 调度
    def run(self):
        # 开始时间
        self.start_time = time.time()

        # 1.请求
        self.driver.get(self.url)

        # 2.获取数据
        data = self.driver.page_source

        # 3.解析数据
        result_list = self.parse_data(data)

        # 4.保存数据
        self.write_file(result_list)

        # 循环发送请求　获取所有页面的数据

        # 多线程　实现异步任务
        for i in range(5):
            self.pool.apply_async(self.execute_request_save, callback=self._callback)

        # 阻塞主线程  python3中主线程结束，子线程不结束。
        while True:
            # 防止cpu空转
            time.sleep(0.001)
            if self.driver.find_element_by_xpath('//span[text()="下一页"]/..').get_attribute('aria-disabled') == 'true':
                break

        # 关闭浏览器
        self.driver.quit()

        print('总共{}页数据'.format(self.count))
        # 结束时间
        self.end_time = time.time()

        print('运行程序总共花了{}s'.format(self.end_time - self.start_time))


if __name__ == '__main__':
    DouYuSpider().run()