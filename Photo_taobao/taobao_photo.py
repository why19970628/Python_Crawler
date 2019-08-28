from urllib import request
import urllib
import urllib.parse
import re
from urllib.error import URLError
key='连衣裙'
key=urllib.request.quote(key)
headers=('user-agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
urllib.request.install_opener(opener)
for i in range(1,20):
    url='https://re.taobao.com/search?spm=a231k.8165028.0782702702.204.60792e63WFZKub&prepvid=300_11.10.228.22_44360_1543657608665&extra=&keyword='+key+'&frontcatid=&isinner=1&refpid=420435_1006&page='+str(i)+'&rewriteKeyword&_input_charset=utf-8'
    print(url)
    data=urllib.request.urlopen(url).read().decode('utf-8','ignore')
    #pat='<a href="(.*?)"'
    pat='img data-ks-lazyload="(.*?)_260x260.jpg'
    image_url=re.compile(pat).findall(data)
    for j in range(0,len(image_url)):
        this_img=image_url[j]
        file='./taobao_photo/'+str(i)+str(j)+'.jpg'
        urllib.request.urlretrieve(this_img,filename=file)
    print(image_url)
