import requests
import re
import json
import pandas as pd
url=''
headers={'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
def get_info(id):
    res=requests.get('http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1'.format(id),headers=headers)
    json_data=json.loads(res.text)
    lyric=json_data['lrc']['lyric']
    lyric=re.sub('\[.*\]','',lyric)
    return  str(lyric)
def txt():
    data=pd.read_csv('music.csv')
    for i in range(len(data['song_id'])):

            fp=open(r'歌词/{}.txt'.format(data['song'][i]),'w',encoding='utf-8')
            fp.write(get_info(data['song_id'][i]))
            fp.close()

txt()
