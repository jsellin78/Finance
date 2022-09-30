import time
import datetime
import threading
import requests
import os
import subprocess

chat_id="2012646742" #Enter Telegramchat_id
TOKEN="5640166055:AAE4vMzP-lk2dh-fszrejyRFBhCCp1UCGXI" #Token

# After the alert is set
# Press Ctrl Z then type bg
# To list all running Alerts type jobs.

def start_timer():
    header = 17 * "-" + "TIME REMINDER!" + 17 * "-"
    underline = 73 * "-"

    print(header)
    year = int(input('Enter a year --> ')) #YYYY

    print(underline)
    month = int(input('Enter a month --> ')) # 1 to 12

    print(underline)
    day = int(input('Enter a day --> ')) # 1 to 31

    print(underline)
    hour = int(input('Enter an hour --> ')) # 0 to 23

    print(underline)
    minute = int(input('Enter a minute --> ')) # 0 to 59

    print(underline)
    description = str(input('Enter description --> ')) # Description of message

    startTime = datetime.datetime(year, month, day, hour, minute)
    print(" ~~> Telegram Alert is set from: {}".format(startTime))
    print(" ~~> now: {}".format(datetime.datetime.now()))
    print(underline)
    time.sleep(2)

    while datetime.datetime.now() < startTime:
        time.sleep(1)

    print('Time\'s up')
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={description}"
    print(requests.get(url).json())

myTimerThread=threading.Thread(
    target=start_timer,
    name='myTimerThread')
myTimerThread.daemon = True
myTimerThread.start()
myTimerThread.join()
