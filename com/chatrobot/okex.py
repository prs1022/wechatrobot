# encoding:utf8

import requests
import ast

'''
根据币对信息，获取价格和交易量等信息
币对例如 BTC-USTD
'''

# 支持这些币种的大小写和中文输入
instrument_ids = {"OKB": "OKB", "okb": "OKB", "BTC": "BTC", "btc": "BTC",
                  "ETH": "ETH", "eth": "ETH", "LTC": "LTC", "ltc": "LTC",
                  "BCH": "BCH", "bch": "BCH", "ETC": "ETC", "etc": "ETC",
                  "XRP": "XRP", "xrp": "XRP", "EOS": "EOS", "eos": "EOS",
                  "ONT": "ONT", "ont": "ONT", "TRX": "TRX", "trx": "TRX",
                  "比特币": "BTC", "以太坊": "ETH", "柚子": "EOS", "小姨太": "ETC",
                  "瑞波": "TRX", "瑞波币": "TRX", "莱特币": "LTC", "莱特": "LTC", "辣条": "LTC",
                  "碧池": "BCH", "牛B": "OKB"
                  }

# 交割合约币种
future_instrument_ids = {"季度": "-190329", "当周": "-190315", "次周": "-190322"}

type_ids = {"现货": "spot", "交割合约": "futures"}

# 平台币
pingtaicoin = ["okb","OKB","BNB","bnb","HT","ht"]

def get_ticket(instrument_id, type):
    if type == '交割合约':
        instrument_id = instrument_id.__add__("-USD-190329") #默认都是季度合约
    else:
        if "-" not in instrument_id:  # 默认交易对是输入的+USDT
            instrument_id = instrument_id.__add__("-USDT")
    response = requests.get("https://www.okex.me/api/%s/v3/instruments/%s/ticker" % (type_ids[type], instrument_id))
    content_str = response.content.decode("utf-8")
    content = ast.literal_eval(content_str)
    return ("最新成交价:%s刀\n24小时高低价:%s,%s\n24小时%s交易量:%s"
            % (content["last"], content["high_24h"], content["low_24h"], content["instrument_id"].split("-")[0],
               content["base_volume_24h"]))

def get_pingtaicoin():
    okb_res = requests.get("https://www.okex.me/api/%s/v3/instruments/%s/ticker" % ("spot", "OKB-USDT"))
    bnb_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT")
    ht_res = requests.get("https://api.huobi.pro/market/detail/merged?symbol=htusdt")
    okb_ast = ast.literal_eval(okb_res.content.decode("utf-8"))
    ht_content = ast.literal_eval(ht_res.content.decode("utf-8"))["tick"]
    result=""
    result = result.__add__("OKB-> 现价:%s,成交量:%s\nBNB-> 现价:%s\nHT-> 现价:%s,成交量:%s" % (cut_two_digits(okb_ast["last"]),cut_two_digits(okb_ast["base_volume_24h"]),
                                                                                  cut_two_digits(ast.literal_eval(bnb_res.content.decode("utf-8"))["price"])
                                                ,cut_two_digits(ht_content["close"]),cut_two_digits(ht_content["amount"])))
    return result

def gonglian_coin():
    ont_res = requests.get("https://www.okex.me/api/%s/v3/instruments/%s/ticker" % ("spot", "ONT-USDT"))
    btm_res = requests.get("https://www.okex.me/api/%s/v3/instruments/%s/ticker" % ("spot", "BTM-USDT"))

    result=""
    return result.__add__("ONT-> 现价:%s,成交量:%s\nBTM-> 现价:%s,成交量:%s"
                          % ())

# 截取数字的后小数点后两位
def cut_two_digits(number):
    number = str(number)
    if '.' in number:
        return number[:number.find('.')+3]
    return number

if __name__ == '__main__':
    # print(get_ticket("OKB-USDT"))
    print(get_pingtaicoin())
