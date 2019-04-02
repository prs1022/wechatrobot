# encoding: utf-8
import urllib.request
import requests
import time
import schedule
import datetime
import json
from aip import AipOcr
import ssl
import re
from io import BytesIO

# ssl._create_default_https_context = ssl._create_unverified_context  # 取消全局验证

verify_IMG_ID = "img_code"
img_url = ""
refer = "https://www.douban.com/group/topic/xx/?start=0"  # 正常访问的refer
cookie = ''


def job():
    global verify_IMG_ID, img_url, refer, cookie
    url = "https://www.douban.com/group/topic/xx/add_comment"
    headers = {
        "Host": "www.douban.com",
        "Referer": refer,
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    params = {
        "ck": "jhb4",
        "rv_comment": "up " + current_time,
        "start": 0,
        "img": "(binary)",
        "captcha-solution": text_identify(img_url).__str__(),  # 验证码的解析文本
        "captcha-id": verify_IMG_ID,  # 验证码图片ID
        "submit_btn": "发送"
    }

    """ 在豆瓣多次调用评论接口后会返回一个页面，需要输入验证码，从页面里我们解析dom信息拿到验证码图片的URL，然后读取成图片，解析文本"""

    response = requests.post(url, headers=headers, allow_redirects=False, data=params, verify=False)
    print(response)
    if response.__str__().__contains__("200"):  ## 需要验证码
        searchObj = re.search(r'(.*)(https://www.douban.com/misc/captcha)(.*?)(alt="captcha").*',
                              response.content.__str__(), re.M | re.I)
        img_url = searchObj.group(2) + searchObj.group(3)  # 图片URL
        print("imgURL->" + img_url)
        verify_IMG_ID = searchObj.group(3)[4:4 + 27]
        print("imgCode->" + verify_IMG_ID)
        refer = "https://www.douban.com/group/topic/xx/add_comment"


def text_identify(img_url):
    if img_url == '':
        return ""
    ## 自己申请key
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    def get_file_content(file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()  # 返回字节流

    # image = get_file_content(u'C:\\Users\\PC\\Pictures\\textimg.png')

    res = requests.get(img_url,
                       stream=True)  # 获取字节流最好加stream这个参数,原因见requests官方文档

    image = BytesIO(res.content).getvalue()

    """BaiduAPI文字试别"""
    result = client.basicAccurate(image)
    print("result类型:"+str(type(result)))
    if "error_msg" in result.keys():
        print("图片解析错误:"+result['error_msg'])
        return ""
    print("BaiduAPI result>>" + str(result))
    if int(result['words_result_num']):
        text_plain = result["words_result"][0]["words"].strip().replace(".","")
        print("试别结果:%s" % text_plain)
        return text_plain  # 有点奇怪，第一个字符不匹配
    print("未试别:%s" % json.dumps(result))


if __name__ == '__main__':
    print("豆瓣刷评开始---")
    job()
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
