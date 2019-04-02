# encoding:utf8
'''
股票API
太慢了，一次性获取的是全部数据
'''
import requests

if __name__ == '__main__':
    url = "https://api.shenjian.io/?appid=502068e260027c1b4a748cab171c7701"
    gupiao_name="红阳能源"
    response = requests.get(url)
    list = list(str(response["data"]))
    for i in range(len(list)):
        if gupiao_name==list[i]["code"] or gupiao_name==list[i]["name"]:
            print(list[i])
            break
