# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:心蓝
import requests

"""
实现12306网站的登录
"""
map = {
    '1': '37,42',
    '2': '111,42',
    '3': '180,42',
    '4': '254,42',
    '5': '37,118',
    '6': '111,118',
    '7': '180,118',
    '8': '254,118',
}


def get_point(indexs):
    """
    根据输入的序号获取相应的坐标
    :param indexs: 1,2
    :return:
    """
    indexs = indexs.split(',')
    temp = []
    for index in indexs:
        temp.append(map[index])
    return ','.join(temp)


# cookie 保持 浏览器
session = requests.Session()

# 伪装
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
session.headers.update(headers)
# 1.访问登录页面
login_url = 'https://kyfw.12306.cn/otn/login/init'
session.get(login_url)

# 2.下载验证码图片
captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5846169880733507'
captcha_response = session.get(captcha_url)

with open('captcha.jpg', 'wb') as f:
    f.write(captcha_response.content)

# 3.校验验证码
check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
form_data = {
    'answer': get_point(input('请输入正确的序号>>>:')),
    'login_site': 'E',
    'rand': 'sjrand'
}
check_response = session.post(check_captcha_url, data=form_data)
#print(check_response.json())
if check_response.json()['result_code'] == '4':  #'result_message': '验证码校验成功', 'result_code': '4'
    # 校验成功
    # 4.校验用户名和密码
    login_url = 'https://kyfw.12306.cn/passport/web/login'
    form_data = {
        'username': '你的账号',
        'password': '你的密码',
        'appid': 'otn'
    }
    login_response = session.post(login_url, data=form_data)
    print(login_response.json())
    #'result_message': '登录成功', 'result_code': 0, 'uamtk': '0YeWhGwOquOICVxAQZz0NxXSX6a_0AJcOBG6zfDMNsolm1210'
    if login_response.json()['result_code'] == 0:

        # 5.获取 权限 token
        uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        uamtk_response = session.post(uamtk_url, data={'appid': 'otn'})
        #print(uamtk_response.json())
        #'result_message': '验证通过', 'result_code': 0, 'apptk': None, 'newapptk': '-oTvBp0Sfb_LwV6irTcmGcf9jtyO5W_xykRJNL2t4Gk511210'
        if uamtk_response.json()['result_code'] == 0:
            # 6.校验token
            check_token_url = 'https://kyfw.12306.cn/otn/uamauthclient'
            check_token_response = session.post(check_token_url, data={'tk': uamtk_response.json()['newapptk']})
            print(check_token_response.json())

