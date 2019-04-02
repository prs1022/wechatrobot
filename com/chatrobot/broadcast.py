# encoding: utf-8

import requests


## 根据cityCode获取天气情况
city_codes = {}

def getWeather(cityCode):
    data = {}
    response = requests.get(url="http://t.weather.sojson.com/api/weather/city/" + str(cityCode), params=data)
    dataMap = response.json()["data"]
    shidu = dataMap["shidu"]  # 湿度
    quality = dataMap["quality"]  # 污染程度
    wendu = dataMap["wendu"]  # 温度
    curr = dataMap["forecast"][0]
    sunrise = curr["sunrise"]
    high = curr["high"]
    low = curr["low"]
    sunset = curr["sunset"]
    week = curr["week"]
    type = curr["type"]  # 天气情况
    notice = curr["notice"]

    return ("当前城市:" + response.json()["cityInfo"]["city"] + " " + week + "\n小猪报天气^(* (oo) )^:\n"
            + type + "," + wendu + "℃\n"
            + "湿度:" + shidu + "\n"
            + "空气质量:" + quality + "\n"
            + high + "," + low + "\n"
            + "日出:" + sunrise + " 日落:" + sunset
            + "\n小猪温馨提示:" + notice
            )


def initCityCode():
    f = open("city_code.txt", 'r', encoding="utf-8")  # 返回一个文件对象
    line = f.readline()
    global city_codes
    while line:
        split = line.split("=")
        city_codes[split[1].__str__().replace("\n", "")] = split[0].__str__()
        line = f.readline()



