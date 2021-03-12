from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import sys

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    try:
        r = requests.get('https://rtxscalping.herokuapp.com/check')
    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()


@sched.scheduled_job('interval', minutes=30)
def remove_slugs():
    try:
        r = requests.get('https://rtxscalping.herokuapp.com/cleanup')
    except requests.exceptions.RequestException as e:
        print(e)
        sys.stdout.flush()


sched.start()
