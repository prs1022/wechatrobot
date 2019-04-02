# encoding:utf8

import requests
'''
星座今日运势
'''
def yunshi_today(name):
    xz_name= str(name)
    if xz_name.endswith("座") is False:
         xz_name = xz_name.__add__("座")
    response = requests.get("https://api.shenjian.io/constellation/today?appid=${your own appId}",
                       {"constellation": xz_name})
    content = response.content.decode("utf-8")
    fate_data_ = eval(content)["data"]["fate_data"]
    result = ""
    for i in range(len(fate_data_)):
        result = result.__add__(fate_data_[i]["name"]+fate_data_[i]["value"]+"\n")
    result =  result.__add__(",".join(eval(content)["data"]["lucky_object"]))
    return result


if __name__ == '__main__':
    print(yunshi_today("射手"))