# coding = utf-8
import os
import time

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv(".env")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route("/kasikorn", methods=["GET"])
def kasikorn():
    key = request.headers.get('x-api-key')
    if key != os.getenv('API_KEY'):
        return 'Invalid apikey'
    url = "https://www.kasikornbank.com/en/Rate/Pages/Foreign-Exchange.aspx"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
    }
    r = requests.get(url, headers=headers)
    html = r.content.decode('utf-8', 'ignore')
    page = BeautifulSoup(html, 'lxml')
    list = page.find("div", id="divLastRate")
    obj = {}
    if list:
        rate = list.find_all("div")
        n = 0
        obj = {}
        currency = ['USD 50-100', 'CNY', 'SGD', 'MYR', 'RUB', 'HKD', 'TWD']
        for i, item in enumerate(rate):
            if n >= 7:
                break
            unit = item.get("data-sname").strip()
            if unit in currency:
                buy_price = item.get("data-buybn").strip()
                sell_price = item.get("data-sellbn").strip()
                if unit == 'USD 50-100':
                    unit = 'USD'
                if buy_price != '-':
                    obj[unit+'THB'] = float(buy_price)
                if sell_price != '-':
                    obj['THB'+unit] = float(round(1 / float(sell_price), 4))
                n = n + 1
    return jsonify(obj)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT'), debug=True)