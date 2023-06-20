import time
import ujson
import sys
import multiprocessing
import argparse
import requests
import math
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

#python3 ./pricealert.py --currency=usdsek --target=1.20000 --timeout=86400 --workers=2 --type=below --interval=2 & 

chat_id = ""  # Telegram chat_id
TOKEN = ""  # Token
session = requests.Session()

logging.basicConfig(filename='price_alert.log', level=logging.DEBUG)


def get_price_info():
    url = "ws://192.168.1.220:8015/posts"
    response = session.get(url)
    data = response.json()
    time_str = data['time']
    prices = data.copy()
    del prices['time']
    return time_str, prices


def send_telegram_alert(currency, current_price, target_price, time_str, alert_type, pattern_date):
    if alert_type == 'below':
        message = f"Price Alert for {currency}! Current price: {current_price:.5f} is below target price: {target_price:.5f} as of {time_str} created at {pattern_date}"
    elif alert_type == 'above':
        message = f"Price Alert for {currency}! Current price: {current_price:.5f} is above target price: {target_price:.5f} as of {time_str} created at {pattern_date}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    response = session.get(url)
    if response.status_code == 200:
        print(message)
        logging.info(message)
    else:
        logging.error(f'Error: Failed to send message. Status code: {response.status_code}')


def price_alert(args):
    currency, target_price, max_run_time, alert_type, wait_time, pattern_date = args
    start_time = time.monotonic()

    def check_prices():
        time_str, prices = get_price_info()
        if prices.get(currency):
            if alert_type == 'below' and prices[currency] < target_price:
                # trigger an alert (e.g. send a Telegram message)
                send_telegram_alert(currency, prices[currency], target_price, time_str, alert_type, pattern_date)
                scheduler.shutdown()
            elif alert_type == 'above' and prices[currency] > target_price:
                # trigger an alert (e.g. send a Telegram message)
                send_telegram_alert(currency, prices[currency], target_price, time_str, alert_type, pattern_date)
                scheduler.shutdown()

    # Schedule the check_prices function to run at the specified interval
    trigger = IntervalTrigger(seconds=wait_time)
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_prices, trigger)
    scheduler.start()

    # Run the scheduler for the specified maximum run time
    time.sleep(max_run_time)
    scheduler.shutdown()


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

    print(f"Currency: {args.currency}")
    print(f"Import time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    # Create a list of arguments for each worker process to minimize CPU usage
    worker_args = [(args.currency, args.target_price, args.max_run_time, args.alert_type, args.wait_time, args.pattern_date) for i in range(args.workers)]

    # Create a Pool of worker processes and run the `price_alert` function with each set of arguments
    with multiprocessing.Pool(args.workers) as p:
        p.map(price_alert, worker_args)

if __name__ == '__main__':
    main()


            
