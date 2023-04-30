import time
import json
import os 
import sys
import multiprocessing 
import argparse
import requests
import math

chat_id="" #Telegramchat_id
TOKEN="" #Token

#python3 ./priceAlert.py --file=/root/tmp/currency.txt --currency=usdsek --target=1.20000 --timeout=86400 --workers=2 --type=above --interval=180 & 


def get_last_line(file_path):
    with open(file_path, 'rb') as file:
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR)
        last_line = file.readline().decode().strip()
        return last_line

def parse_price_info(price_info):
    data = json.loads(price_info)
    time_str = data['Time']
    prices = data.copy()
    del prices['Time']
    return time_str, prices

def price_alert(args):
    file_path, currency, target_price, max_run_time, alert_type, wait_time = args
    start_time = time.time()
    while time.time() - start_time < max_run_time:
        last_line = get_last_line(file_path)
        time_str, prices = parse_price_info(last_line)
        tolerance = 1e-5
        if prices.get(currency):
            if alert_type == 'below' and math.isclose(prices[currency], target_price, rel_tol=1e-5):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text='Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}'"
                requests.get(url).json()
                print(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}')
                print("Target price reached. Stopping the script...")
                break
            elif alert_type == 'above' and math.isclose(prices[currency], target_price, rel_tol=1e-5):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text='Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}'"
                requests.get(url).json()
                print(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is above target price: {target_price:.5f} as of {time_str}')
                print("Target price reached. Stopping the script...")
                break
        time.sleep(wait_time)

def main():
    parser = argparse.ArgumentParser(description='Run price alert.')
    parser.add_argument('--file', dest='file_path', help='Path to the file with price information', required=True)
    parser.add_argument('--currency', dest='currency', help='Currency to monitor', required=True)
    parser.add_argument('--target', dest='target_price', type=float, help='Target price for the currency', required=True)
    parser.add_argument('--timeout', dest='max_run_time', type=int, help='Maximum run time in seconds', required=True)
    parser.add_argument('--workers', dest='workers', type=int, help='Number of worker processes', required=True)
    parser.add_argument('--type', dest='alert_type', choices=['above', 'below'], help='Type of price alert (above/below target price)', required=True)
    parser.add_argument('--interval', dest='wait_time', type=int, help='Time to wait between checking prices (in seconds)', default=300)

    args = parser.parse_args()

    # Create a list of arguments for each worker process to minimize cpu usage 
    worker_args = [(args.file_path, args.currency, args.target_price, args.max_run_time, args.alert_type, args.wait_time) for i in range(args.workers)]

    # Create a Pool of worker processes and run the `price_alert` function with each set of arguments
    with multiprocessing.Pool(args.workers) as p:
        for _ in p.imap(price_alert, worker_args, chunksize=1):
            pass

if __name__ == '__main__':
    main()
