import responder
import requests
import sys
import os
from time import time
from scalp import scalp, cleanup

api = responder.API()

@api.route('/')
def index(req, resp):
    scalp_values = process_scalp()
    resp.html = api.template('index.html', scalp_values=scalp_values,
        spontit_url=os.environ['SPONTIT_INVITE_URL'])


def process_scalp():
    scalp_values = {}
    try:
        r = requests.get(os.environ['POWER_URL'] + str(time()))
        r = r.json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()
        return ""
    for prod in r['Products']:
        if prod['StockCount'] > 0:
            scalp_values[prod['TitleSlug']] = {
                "title": prod['Title'],
                "url": prod['Url'],
                "amount": prod['StockCount']
                }
    return scalp_values

@api.route('/check')
def check(req, resp):
    @api.background.task
    def checker():
        scalp()
    resp.content = "processing scalp"

@api.route('/cleanup')
def cleanup(req, resp):
    @api.background.task
    def cleaner():
        cleanup()
    resp.content = "processing cleanup"

if __name__ == "__main__":
    api.run()
