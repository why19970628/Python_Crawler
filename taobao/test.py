import requests
import pprint
from lxml import etree
import json
import urllib
from  urllib import request
headers={
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"t=4f8e0f1ccaf38c3b87096409eeb1fd52; cna=FOKyFcj3bnQCAdocR8ZpjqDM; tracknick=%5Cu6211%5Cu53EB%5Cu738B%5Cu5927%5Cu9633%5Cu554A; lgc=%5Cu6211%5Cu53EB%5Cu738B%5Cu5927%5Cu9633%5Cu554A; tg=0; thw=cn; cookie2=1515a17feb4817e0b121ec61c57bdebd; _tb_token_=f346348eef015; _m_h5_tk=60367eb5c8d7c62be5befdf974af4201_1564038274783; _m_h5_tk_enc=9e7a36f5498b1568032367f248ae47ee; uc3=lg2=UIHiLt3xD8xYTw%3D%3D&id2=UUGrdwHsJB6u%2BQ%3D%3D&nk2=rUszGXlaengSz%2BTL&vt3=F8dBy3zbW%2FWdhdBl7NE%3D; uc4=nk4=0%40r7q1NfecRXnYVq4toteFS9tFPfXPIO4%3D&id4=0%40U2OcR2VRIfPxS27lnuSvz1%2BkOUiV; _cc_=U%2BGCWk%2F7og%3D%3D; enc=4wio677EOfwVE4ZtLJjx3w0OUX9gNfrhOPqVwF%2B6OyFs7QlbFG02LVHBZ7Ap4D9cFy7VZetUXAs0oBAAYBuTDQ%3D%3D; mt=ci=104_1; swfstore=307564; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; whl=-1%260%260%261564031467353; uc1=cookie14=UoTaHPgonNb53g%3D%3D; v=0; pnm_cku822=098%23E1hvrvvUvbpvUvCkvvvvvjiPRFFvsjiRnLdU1jD2PmPW0jrPP2zO1jDnRLLZtjY8iQhvChCvCCptvpvhphvvv8yCvv3vpvo1y6cQtOyCvvXmp99hetutvpvIphvvvvvvphCvpv3cvvChXZCvjvUvvhL6phvwv9vvBW1vpCQmvvChsvyCvh1hAXyvI1QaUjCwiNoOejaPJHLXSfpAOHCqVUcn%2B3C1osEc6aZtn0vHVA3lYb8rwo1%2Bm7zhdigDN5WK%2BE7reB69EcqhaB4AVAWaUExrvphvCyCCvvvvvvGCvvpvvPMM; l=cBTrwufVqMp97_ASXOCwourza77OSIRAguPzaNbMi_5BU6L1UuQOkVGcNFp6VjWd9hYB4sdB3ey9-etkiWMuGiuXppgF.; isg=BFRUAAxi9T5QyWF9SrxZjDUFJZLGrXiXR5zNBu414F9i2fQjFr1IJwpb2ZFkIbDv",
"Host":"shop130809627.taobao.com",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
}
url='https://shop130809627.taobao.com/i/asynSearch.htm?_ksTS=1564031496810_573&callback=jsonp574&mid=w-18789199391-0&wid=18789199391&path=/category.htm&spm=a1z10.3-c-s.w4002-18789199391.25.300342a2PK2mOr&orderType=hotsell_desc'
#req = request.Request(url, headers=headers)
#html = request.urlopen(req).read().decode()
#print(html)
s= requests.session()
res =s.get(url,headers=headers,verify=False)
res.encoding='utf-8'
#res=json.load(res)
html=res.text
print(html)
import re
a=r'.*?<span class=\"c-price\">(.*?)</span></div>.*?'
con=re.compile(a,re.S)
links = re.findall(con, html)
print(links)