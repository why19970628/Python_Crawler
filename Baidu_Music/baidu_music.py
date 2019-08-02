import requests
import re,json,pprint,os
#url='http://zhangmenshiting.qianqian.com/data2/music/a612909cdafecf20933bd2942c43421c/596603939/596603939.mp3?xcode=10263e95dfecc6e6f4316fffb8ff8771'
def download_music(songid):
    url='http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery17208091693203165158_1545207385401&songid='+songid+'&from=web&_=1545207388641'
    url2='href="http://music.163.com/song/media/outer/url?id=317151.mp3'
    response=requests.get(url)
    data=json.loads(re.findall("{.*}",response.text)[0])
    music_name=data['songinfo']['title']
    artist=data['songinfo']['artist']
    music_url=data['bitrate']['file_link']
    #pprint.pprint(data)
    return music_name,music_url,artist
#music_name,music_url=download_music('265715650')
#print(music_name,music_url,)
def get_songid(artist_id):
    for i in range(0, 41, 20):
        reponse=requests.get(url="http://music.taihe.com/artist/"+artist_id)
        #print(reponse.text)#ctrl+u 查看网页源代码
        songids=re.findall('{&quot;id&quot;:&quot;(.*)&quot;,&quot;kr_top&quot;',reponse.text)
        return  songids
def save_music(music_name,music_url,artist):
    music_res = requests.get(music_url)
    try:
        folder = os.path.exists(artist)

        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(artist)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print
            "---  new folder...  ---"
            print
            "---  OK  ---"

        else:
            print
            "---  There is this folder!  ---"

        file = "D:/软件（学习）/Python/TanZhou/百度音乐/" + artist + '/' + music_name + ".mp3"
        with open(file,'wb') as f:
            f.write(music_res.content)
    except:
        print('下载失败')
def run():
    artist_id=input('请输入网易歌手ID:')
    singids=get_songid(artist_id)
    for songid in singids:
        music_name, music_url,artist=download_music(songid)
        save_music(music_name, music_url,artist)
        print(music_name + "  下载完成")
run()



