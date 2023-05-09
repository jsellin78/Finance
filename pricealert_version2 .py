import time 
import ujson  
from os import SEEK_CUR, SEEK_END
import sys
import multiprocessing 
import argparse
import requests
import math
import logging
import time

chat_id="2012646742" #Enter Telegramchat_id
TOKEN="5640166055:AAE4vMzP-lk2dh-fszrejyRFBhCCp1UCGXI" #Token
session = requests.Session()

logging.basicConfig(filename='price_alert.log', level=logging.DEBUG)


def get_price_info():
    url = "http://192.168.1.220:8013/posts"
    response = session.get(url)
    data = response.json()
    time_str = data['time']
    prices = data.copy()
    del prices['time']
    return time_str, prices

def price_alert(args):
    currency, target_price, max_run_time, alert_type, wait_time, pattern_date = args
    start_time = time.time()
    while time.time() - start_time < max_run_time:
        time_str, prices = get_price_info()
        tolerance = 1e-4
        if prices.get(currency):
            if alert_type == 'below' and math.isclose(prices[currency], target_price, rel_tol=1e-4):
                # trigger an alert (e.g. send a Telegram message)
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text='Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str} created at {pattern_date}'"
                response = session.get(url)
                if response.status_code == 200:
                    print(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str} created {pattern_date}')
                    alert_triggered = True
                    #print("Target price reached. Stopping the script...")
                    break
                else:
                    logging.error(f'Error: Failed to send message. Status code: {response.status_code}')
            elif alert_type == 'above' and math.isclose(prices[currency], target_price, rel_tol=1e-4):
                # trigger an alert (e.g. send a Telegram message)
                if response.status_code == 200:
                    logging.info(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is above target price: {target_price:.5f} as of {time_str}')
                    logging.info("Target price reached. Stopping the script...")
                    alert_triggered = True
                    break
                else:
                    logging.error(f'Error: Failed to send message. Status code: {response.status_code}')
        time.sleep(wait_time)


def main():
    parser = argparse.ArgumentParser(description='Run price alert.')
    parser.add_argument('--currency', dest='currency', help='Currency to monitor', required=True)
    parser.add_argument('--target', dest='target_price', type=float, help='Target price for the currency', required=True)
    parser.add_argument('--timeout', dest='max_run_time', type=int, help='Maximum run time in seconds', required=True)
    parser.add_argument('--workers', dest='workers', type=int, help='Number of worker processes', required=True)
    parser.add_argument('--type', dest='alert_type', choices=['above', 'below'], help='Type of price alert (above/below target price)', required=True)
    parser.add_argument('--interval', dest='wait_time', type=int, help='Time to wait between checking prices (in seconds)', default=300)
    parser.add_argument('--patterndate', dest='pattern_date', type=str, help='Pattern date for the currency', required=True)
    args = parser.parse_args()

    # Create a list of arguments for each worker process to minimize cpu usage 
    worker_args = [(args.currency, args.target_price, args.max_run_time, args.alert_type, args.wait_time, args.pattern_date) for i in range(args.workers)]

    # Create a Pool of worker processes and run the `price_alert` function with each set of arguments
    with multiprocessing.Pool(args.workers) as p:
        for _ in p.imap(price_alert, worker_args, chunksize=1):
            pass

if __name__ == '__main__':
    main()        
