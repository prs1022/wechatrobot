# encoding:utf8

import requests
import re

'''
根据手机号查询归属地（省份、城市）和手机卡类型
'''


def mobile_info(phone_number):
    response = requests.get(
        "http://ws.webxml.com.cn/WebServices/MobileCodeWS.asmx/getMobileCodeInfo?mobileCode=%s&userID=" % phone_number)
    content = response.content.decode("utf-8")
    return content[content.find(phone_number[0:4]):content.find("</string",content.find(phone_number[0:4]))]

if __name__ == '__main__':
    print(mobile_info("1111152517103791"))