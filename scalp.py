import os
import redis
import spontit
import requests
from time import time, sleep
from urllib.parse import urlparse
from spontit import SpontitResource
from datetime import datetime, timedelta

url = urlparse(os.environ.get("REDIS_URL"))
red = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)
notify = SpontitResource('rtxscalping', os.environ['SPONTIT_KEY'])

def scalp():
    try:
        r = requests.get(os.environ['POWER_URL'] + str(time()))
        r = r.json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()
        return ""
    for prod in r['Products']:
        if prod['StockCount'] > 0:
            if not red.exists('in_stock', prod['TitleSlug']):
                red.lpush('in_stock', prod['TitleSlug'])
                msg = """
                IN STOCK: {stock_count}
                     - NAME: {title}
                     - URL: https://www.power.dk{url}
                ------------------------------------------------------
                """.format(
                stock_count = prod['StockCount'],
                title = prod['Title'],
                url = prod['Url']
            )
            print(msg)
            notify.push(
                push_content=prod['Title'],
                link="https://www.power.dk{}".format(prod['Url']),
                should_open_link_in_app=False,
                content=msg)

def cleanup():
    try:
        r = requests.get(os.environ['POWER_URL'] + str(time()))
        r = r.json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()
        return ""
    for prod in r['Products']:
        for slug in prod['TitleSlug']:
            if red.exists('in_stock', slug):
                if prod['StockCount'] == 0:
                    print("Removing {} from list out of stock.".format(prod['TitleSlug']))
                    red.lpop('in_stock', slug)
