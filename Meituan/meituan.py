import csv
import time
import threading
from get_cookie import get_cookie
from get_cookie import parse


def crow(n, l):  # 参数n 区分第几个线程，l存储url的列表
    lock = threading.Lock()
    sym = 0  # 是否连续三次抓取失败的标志位
    pc = get_cookie()  # 获取IP 和 Cookie
    m = 0  # 记录抓取的数量
    now = time.time()
    while True:
        if len(l) > 0:
            u = l.pop(0)
            ll = len(l)
            m += 1
            ttt = time.time() - now
            result = parse(u, pc, m, n, ll, ttt)
            mark = result[0]
            info = result[1]
            if mark == 2:
                time.sleep(1.5)
                result = parse(u, pc, m, n, ll, ttt)
                mark = result[0]
                info = result[1]
                if mark != 0:
                    sym += 1
            if mark == 1:
                pc = get_cookie()
                result = parse(u, pc, m, n, ll, ttt)
                mark = result[0]
                info = result[1]
                if mark != 0:
                    sym += 1
            if mark == 0:  # 抓取成功
                sym = 0
                lock.acquire()
                with open('meituan.csv', 'a', newline='', encoding='gb18030')as f:
                    write = csv.writer(f)
                    write.writerow(info)
                f.close()
                lock.release()
            if sym > 2:  # 连续三次抓取失败，换ip、cookie
                sym = 0
                pc = get_cookie()
        else:
            print('&&&&线程：%d结束' % n)
            break


if __name__ == '__main__':
    url_list = []
    with open('mt_id.csv', 'r', encoding='gb18030')as f:
        read = csv.reader(f)
        for line in read:
            d_list = ['', '']
            url = 'https://meishi.meituan.com/i/poi/' + str(line[2]) + '?ct_poi=' + str(line[3])
            d_list[0] = url
            d_list[1] = line[1]
            url_list.append(d_list)
        f.close()
    th_list = []
    for i in range(1, 6):
        t = threading.Thread(target=crow, args=(i, url_list,))
        print('*****线程%d开始启动...' % i)
        t.start()
        th_list.append(t)
        time.sleep(30)
    for t in th_list:
        t.join()
