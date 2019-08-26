#!python3
import random
from urllib.request import ProxyHandler, build_opener
from bs4 import BeautifulSoup
import xlwt
def get_ip():
    fr=open('D:\软件（学习）\Python\PyCharm\kaoshi\ip.txt','r')
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
fo=open('2.html','r',encoding='utf-8')
html=fo.read()
soup=BeautifulSoup(html,'lxml')
fo.close()
#opener = build_opener(proxy_handler)
#for i in range(1):
#    url='http://kaijiang.zhcw.com/zhcw/html/3d/list_'+str(i)+'.html'
#    res=request.Request(url)
#    response=opener.open(res).read().decode('utf-8')
#    soup=BeautifulSoup(response,'lxml')
    #print(soup.select('tr'))
#print(soup.select('tr')[2:-1])
pat=''
a=soup.find_all('td',{'style':'padding-left:20px;'})
#print(a)
#for i in a:
#    print(i.text)

def parse_one_page():
    for item in soup.select('tr')[2:-1]:
        i = 0
        yield {

            'time': item.select('td')[i].text,
            'issue': item.select('td')[i + 1].text,
            'digits': item.select('td em')[0].text,
            'ten_digits': item.select('td em')[1].text,
            'hundred_digits': item.select('td em')[2].text,
            'single_selection': item.select('td')[i + 3].text,
            'group_selection_3': item.select('td')[i + 4].text,
            'group_selection_6': item.select('td')[i + 5].text,
            'sales': item.select('td')[i + 6].text,
            'return_rates': item.select('td')[i + 7].text
        }
parse_one_page()
def write_to_excel():


    f = xlwt.Workbook()

    sheet1 = f.add_sheet('3D',cell_overwrite_ok=True)

    row0 = ["开奖日期","期号","个位数","十位数","百位数","单数","组选3","组选6","销售额","返奖比例"]  #写入第一行

    for j in range(0,len(row0)):

        sheet1.write(0,j,row0[j])
    #依次爬取每一页内容的每一期信息，并将其依次写入Excel

        #写入每一期的信息
        i = 0


    for item in parse_one_page():

        sheet1.write(i+1,0,item['time'])

        sheet1.write(i+1,1,item['issue'])

        sheet1.write(i+1,2,item['digits'])

        sheet1.write(i+1,3,item['ten_digits'])

        sheet1.write(i+1,4,item['hundred_digits'])

        sheet1.write(i+1,5,item['single_selection'])

        sheet1.write(i+1,6,item['group_selection_3'])

        sheet1.write(i+1,7,item['group_selection_6'])

        sheet1.write(i+1,8,item['sales'])

        sheet1.write(i+1,9,item['return_rates'])
        i+=1

    f.save('3D.xls')
#write_to_excel()
