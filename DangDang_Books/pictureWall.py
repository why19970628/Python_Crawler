
import os
import time
import math
import pickle
import requests
from PIL import Image


PICDIR = 'pictures'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}


'''图片下载'''
def downloadPics(urls, savedir):
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    for idx, url in enumerate(urls):
        res = requests.get(url, headers=headers)
        with open(os.path.join(savedir, '%d.jpg' % idx), 'wb') as f:
            f.write(res.content)
        time.sleep(0.5)


'''制作照片墙'''
def makePicturesWall(picdir):
    picslist = os.listdir(picdir)
    num_pics = len(picslist)
    print('照片数量',num_pics)
    size = 64
    line_numpics = int(math.sqrt(num_pics))#正方形
    picwall = Image.new('RGBA', (line_numpics*size, line_numpics*size))
    x = 0
    y = 0
    for pic in picslist:
        img = Image.open(os.path.join(picdir, pic))
        img = img.resize((size, size), Image.ANTIALIAS)     #改变图片尺寸
        picwall.paste(img, (x*size, y*size))    #合并图片
        x += 1
        if x == line_numpics:
            x = 0
            y += 1
    print('[INFO]: Generate pictures wall successfully...')
    picwall.save("picwall.png")     #保存图片


if __name__ == '__main__':
    with open('python_61.pkl', 'rb') as f:
        data = pickle.load(f)
    urls = [j[0] for i, j in data.items()]  #加载图片下载 url
    # downloadPics(urls, PICDIR)
    makePicturesWall(PICDIR)