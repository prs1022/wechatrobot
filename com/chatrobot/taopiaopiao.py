# encoding:utf8
import requests
'''
淘票票 最近最热票房信息
"movie_name":"绿皮书",  /*片名*/
"duration":"上映5天",  /*时间*/
"totle_office":"1.40亿",  /*总票房*/
"real_office":"629.69",  /*实时票房(万元)*/
"office_ratio":"29.8%",  /*票房占比*/
"show_rate":"21.1%",  /*排片占比*/
"avg_seat_view":"3.5%"  /*上座率*/
'''

def hot_film():
    response = requests.get("https://api.shenjian.io/promovie/piaofang?appid=${your own appId}") ## 参数appid为自己申请。免费的
    content = response.content.decode("utf-8")
    film_content = eval(content)["data"]
    show_message = ""
    for i in range(len(film_content)):
        item = film_content[i]
        show_message = show_message.__add__("《" + item["movie_name"] + "》," + item["duration"] + ",总票房:"
                                            + item["totle_office"] + "\n")
    return show_message

if __name__ == '__main__':
    print(hot_film())