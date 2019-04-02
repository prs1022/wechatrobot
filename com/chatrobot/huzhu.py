import time
import urllib.request


# okex 小猪助力接口调用
def http_client_post(num):
    restUri = "https://okexcomweb.bafang.com/v2/support/active/annualPig/assist";
    postbody = "assistNo=" + str(num)
    req = urllib.request.Request(url=restUri, data=postbody.encode("utf8"), method="POST")
    req.add_header("Host", "okexcomweb.bafang.com")
    req.add_header("Accept", "*/*")
    req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    req.add_header("User-Agent",
                   "OKEx/2.4.0.1 (iPhone;U;iOS 11.4.1;zh-CN/zh-Hans)locale=zh-Hans statusBarHeight/60 OKApp/(OKEx/2.4.0.1) brokerDomain/www.okex.com brokerId/0 jsbridge/1.0.0 theme/light")
    req.add_header("Referer", "https://okexcomweb.bafang.com/activity/pigGod")
    req.add_header("Authorization","your own token")
    resp = urllib.request.urlopen(req).read()
    return resp.decode("UTF-8")


## 读取互助名单
def read_file():
    f = open("/mingdan20.txt", 'r', encoding="utf-8")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    dict = {}
    while line:
        split = line.split(" ")
        dict[split[1].rstrip()] = split[0].rstrip()
        line = f.readline()
    f.close()
    return dict


def zhuliOne(key):
    return dict(eval(http_client_post(key)))["msg"]


# 发起助力
def zhuli():
    # http_client_post()
    mingdan = read_file()
    # 遍历字典列表
    list = []
    notUp = "达到上限:%s个\n未达到上限：\n"
    count = 0
    for key, values in mingdan.items():
        res = dict(eval(http_client_post(key)))["msg"]
        if res=='':
            res='成功'
        if res.__str__().__contains__("重复助力"):
            notUp = notUp.__add__(key+",")
        if res.__str__().__contains__("上限"):
            count = count + 1
        list.append(values + ",助力结果:" + res)  # 字符串转字典
        time.sleep(1)  # 防止接口繁忙，停顿一秒助力下一位
    list.append(notUp[0:len(notUp)-1] % str(count))
    for item in list:
        print(item + "\n")
    return list


if __name__ == '__main__':
    list = zhuli()
    for item in list:
        print(item + "\n")
