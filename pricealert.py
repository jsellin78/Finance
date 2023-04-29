import time
import json
import os 
import sys
import multiprocessing 
import argparse


#python3 pricealert.py --file /root/tmp/currency.txt --currency usdsek --target 1.20000 --time 3600 --workers 2  

def get_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines() 

def get_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        return last_line

def parse_price_info(price_info):
    data = json.loads(price_info)
    time_str = data['Time']
    prices = data.copy()
    del prices['Time']
    return time_str, prices

def price_alert(args):
    file_path, currency, target_price, max_run_time = args
    start_time = time.time()
    wait_time = 300 
    while time.time() - start_time < max_run_time:
        last_line = get_last_line(file_path)
        time_str, prices = parse_price_info(last_line)
        if prices.get(currency) and prices[currency] < target_price:
            # trigger an alert (e.g. send an email or SMS message)
            print(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}')
            print("Target price reached. Stopping the script...")
            break
        time.sleep(wait_time)

def main():
    parser = argparse.ArgumentParser(description='Run price alert.')
    parser.add_argument('--file', dest='file_path', help='Path to the file with price information', required=True)
    parser.add_argument('--currency', dest='currency', help='Currency to monitor', required=True)
    parser.add_argument('--target', dest='target_price', type=float, help='Target price for the currency', required=True)
    parser.add_argument('--time', dest='max_run_time', type=int, help='Maximum run time in seconds', required=True)
    parser.add_argument('--workers', dest='workers', type=int, help='Number of worker processes', required=True)

    args = parser.parse_args()

    # Create a list of arguments for each worker process to minimize cpu usage 
    worker_args = [(args.file_path, args.currency, args.target_price, args.max_run_time) for i in range(args.workers)]

    # Create a Pool of worker processes and run the `price_alert` function with each set of arguments
    with multiprocessing.Pool(args.workers) as p:
        p.map(price_alert, worker_args)

if __name__ == '__main__':
    main()
