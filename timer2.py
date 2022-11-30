#! /usr/bin/env python3

import time
import os
import sys
from datetime import date
import subprocess
import datetime
import threading
import requests

chat_id="2012646742" #Enter Telegramchat_id
TOKEN="5640166055:AAE4vMzP-lk2dh-fszrejyRFBhCCp1UCGXI" #Token

def start_timer():
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    startTime = datetime.datetime(year, month, day, hour, minute)
    print (" ~~> Telegram Alert is set for:{}".format(startTime))
    while datetime.datetime.now() < startTime:
        time.sleep(1)
    print('Time\'s up')


myTimerThread=threading.Thread(
    target=start_timer,
    name='myTimerThread')
myTimerThread.daemon = True
myTimerThread.start()
myTimerThread.join()
