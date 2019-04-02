# encoding: utf-8
# 源代码如下：
# wechat autoreply
# DOC 查看 https://itchat.readthedocs.io/zh/latest/
import sys
import time

sys.path.append("/home/ftp/app/python_code")
import datetime
import re
import ssl

import itchat
import random

from com.chatrobot.huzhu import zhuli, zhuliOne
from com.chatrobot.broadcast import initCityCode, getWeather, city_codes
from com.chatrobot.taopiaopiao import hot_film
from com.chatrobot.xingzuo import yunshi_today
from com.chatrobot.okex import *
from com.chatrobot.mobiledetail import mobile_info

# python2.7升级到python3需要对ssl进行校验
ssl._create_default_https_context = ssl._create_unverified_context  # 取消全局验证


# 抓取网页
def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# 单个key当天只能回复100条消息
apiKeys = [
    "xxxxxxxxxxxxxxx",
    "xxxxxxxxxxxxxxx",
    "xxxxxxxxxxxxxxx"
]


# 自动回复 [个人消息]
# 封装好的装饰器，当接收到的消息是Text，即文字消息
# Text 文本 视频 Video 文件 attachment 图片picture 名片 card 分享 sharing 语音 recording 地图 Map
@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing', 'Picture'])
def text_reply(msg):
    # 当消息不是由自己发出的时候
    message = msg['Text']
    toName = msg['ToUserName']
    fromName = msg['FromUserName']

    fun_reply = mix_fun(str(message))


    ## git 项目地址
    if message == 'itchat代码':
        return "Git地址:https://github.com/prs1022/wechatrobot";

    if fun_reply != 'null':
        return fun_reply

    '''
    其他消息-图灵机器人回复
    '''
    if apiKeys.__len__() > 0:
        apiKey = apiKeys[0]
    else:
        return  # 没有APIkey的时候直接返回
    if not fromName == Name["小猪佩奇"]:
        print(">>收到%s的消息：%s" % (NickName[fromName], message))
        # 回复给好友
        html = tulingRobotReply(message)
        # print(u"html文本：" + html)
        if html.__contains__("请求次数已用完"):
            apiKeys.remove(apiKey)
            print(u"去除已经达到次数上限的apikey，当前剩余apikey个数:" + len(apiKeys).__str__())
            return
        message = re.findall(r'\"text\"\:\".*?\"', html)
        reply = eval(message[0].split(':')[1])
        print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + "  " + reply)
        time.sleep(2)
        return reply


def tulingRobotReply(text):
    if (apiKeys.__len__() == 0):
        return "今天调戏次数太多，休息了"
    apiKey = apiKeys[0]
    url = u"http://www.tuling123.com/openapi/api?key=" + apiKey + "&info="
    url = url + text
    html = getHtmlText(url)
    return html


## 添加好友
@itchat.msg_register(['FRIENDS'])
def add_friend(msg):
    msg.user.verify()
    msg.user.send(u'Nice to meet you!')


skills = ['[BTC] 查看比特币价格', '[平台币] 查看平台币价格和交易量', '[助力编号] 帮你助力',
          '[上海天气] 查询天气', '[电影票房] 查看最新的电影',
          '[天秤座运势] 查看星座运势', '[手机号前7位] 查询归属地和手机卡类型',
          ]


## 群消息 @ 回复
@itchat.msg_register(['Text'], isGroupChat=True)
def text_reply(msg):
    msg_content = str(msg['Content'])
    msg_text = str(msg['Text'])
    to_user_name = msg['ToUserName']  # 我发消息的时候，toUserName为群
    from_user_name = msg['FromUserName']  # 别人发消息的时候，fromUserName为群
    actual_nick_name = msg['ActualNickName']
    if msg_content == '召唤机器人' or msg_content == '呼叫机器人':
        print("开始发送机器人skills 给" + actual_nick_name + ",来自" + from_user_name)
        itchat.send(u'@' + actual_nick_name + "\n回复[ ]中的内容等待回应\n" + "\n".join(skills), from_user_name)

    fun_reply = mix_fun(msg_content)
    if fun_reply != 'null':
        return fun_reply

    if msg_content == '平台币':
        itchat.send(u'%s' % get_pingtaicoin(), from_user_name)
    # 币圈群发货币代码获取行情h
    query_type = "现货"
    if msg_content.__contains__("季度") or msg_content.__contains__("合约"):
        query_type = "交割合约"
        msg_content = msg_content.replace("季度", "").replace("合约", "")
    if instrument_ids.keys().__contains__(msg_content):
        itchat.send(u'%s' % get_ticket(instrument_ids[msg_content], query_type), from_user_name)
    if msg_content.__contains__("-USDT"):
        itchat.send(u'%s' % get_ticket(msg_content, query_type), from_user_name)

    if msg_content.__contains__('我要助力') or msg_content.__contains__('助力编号'):
        itchat.send(u'@小猪 发助力编号，小猪帮你助力..', from_user_name)
    if msg_content.strip().isdigit() and len(msg_content.strip()) == 8:
        zhuli_res = zhuliOne(msg_content.strip())
        if zhuli_res == '' or len(zhuli_res.strip()) == 0:
            zhuli_res = '成功'
        itchat.send(u'@' + msg['ActualNickName'] + ' 助力结果:' + zhuli_res + ',回助我:70144761', from_user_name)
    if msg_content == 'begin':  ## 自己输入
        list = zhuli()
        list2 = [str(i) for i in list]  # ['a','b','x','y']
        itchat.send(u'%s' % "\n".join(list2), to_user_name)


def mix_fun(msg_content):
    '''
    查询手机号归属地
    '''
    if msg_content.strip().isdigit() and len(msg_content.strip()) >= 7 and len(msg_content.strip()) != 8:
        return mobile_info(msg_content)
    '''
   天气
   :param msg:
   :return:  天气情况
    '''
    if msg_content.__contains__("天气"):
        city_name = msg_content.replace("天气", "")
        if city_name in city_codes.keys():
            return getWeather(city_codes[city_name])
        else:
            noticemsg = ["你是火星来的嘛", "怎么回事，小老弟", "没这个城市", "sorry,not found~"]
            return noticemsg[random.randint(0, 3)]

    '''
    获取电影票房
    '''
    if len(re.findall(".*最近.*电影.*|.*电影.*票房.*|.*好看.*电影.*", msg_content)) > 0:
        return hot_film()

    '''
    星座今日运势
    '''
    if len(re.findall(".*座.*运势.*|.*座", msg_content)) > 0:
        index = msg_content.index('座')
        return yunshi_today(msg_content[index - 2:index])

    return "null"


if __name__ == '__main__':
    initCityCode()  # 启动的时候初始化一次cityCode
    itchat.auto_login(hotReload=True)  # 可以自动重连
    # 获取自己的UserName
    friends = itchat.get_friends(update=True)[0:]
    Name = {}
    Nic = []
    User = []
    NickName = {}
    for i in range(len(friends)):
        Nic.append(friends[i]["NickName"])
        User.append(friends[i]["UserName"])
    for i in range(len(friends)):
        Name[Nic[i]] = User[i]
        NickName[User[i]] = Nic[i]
    itchat.run()
