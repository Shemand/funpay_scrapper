from datetime import datetime

import requests
from bs4 import BeautifulSoup

def crawl():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    }

    server_list = []

    url = "https://funpay.ru/chips/8/"

    try:
        req = requests.get(url=url, headers=headers, timeout=30)
    except requests.exceptions.ConnectionError:
        print('Connection Error: ' + str(datetime.now()))
        return None
    except Exception as err:
        print('Any connection error: ' + str(datetime.now()))
        print(err)
        return None
    req_text = req.text

    soup = BeautifulSoup(req_text, "html.parser")

    all_table = soup.find_all("a", class_="tc-item")
    for item in all_table:
        table_headers = {}

        server = item.find("div", class_="tc-server").text
        table_headers["server"] = server

        salesman = item.find("div", class_="media-user-name").text
        table_headers["user"] = {}
        table_headers["user"]['name'] = salesman

        quantity = item.find("div", class_="tc-amount").text
        quantity = quantity.replace(" кк", "")
        table_headers["quantity"] = float("".join(quantity.split(' '))) / 1000

        price = item.find("div", class_="tc-price").find("div").text
        price = price.replace(" ₽", "")
        table_headers["price"] = float(price)

        id = item.attrs['href']
        string_begin_symbols = '?id='
        id = id[id.find(string_begin_symbols)+len(string_begin_symbols):]
        table_headers['id'] = id

        server_list.append(table_headers)
    return server_list

