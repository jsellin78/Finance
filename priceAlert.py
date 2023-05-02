import time
import ujson  
from os import SEEK_CUR, SEEK_END
import sys
import multiprocessing 
import argparse
import requests
import math

session = requests.Session()
chat_id="" #Telegramchatid
token="" #Token

#python3 ./priceAlert.py --file=/root/tmp/currency.txt --currency=usdsek --target=1.20000 --timeout=86400 --workers=2 --type=above --interval=180 & 

#jsonstring from file {"Time":"2023-05-01 01:13","us30":34093.0,"gbpjpy":171.198,"gbpusd":1.25628,"cadjpy":100.59,"usdjpy":136.266,"nas100":13238.4,"gbpnzd":2.03217,"usdcad":1.35451,"eurusd":1.10153,"eurchf":0.98478,"euraud":1.66636,"eurgbp":0.87671,"eurjpy":150.154,"eurcad":1.492,"nzdusd":0.61805,"audnzd":1.06924,"audusd":0.66097,"xauusd":1990.94,"btcusd":29405.5,"ger40":15940.1,"jpn225":29071.9,"cn50":13209.5,"xngusd":0.0,"gbpcad":1.70159,"gbpaud":1.90034,"eurnzd":1.78187,"audcad":0.89524,"nzdcad":0.83708,"uk100":7867.9,"xpdusd":1499.2,"xptusd":1074.35,"xaujpy":271444.0,"sugar":27.088,"coffee":186.77,"cotton":80.467,"cocoa":2936.6,"wheat":619.8,"soybeans":1446.3,"lumber":463.5,"corn":6.0683,"vix":19.69,"rghrice":17.57,"XAGUSD":25.081,"xaueur":1807.24,"xauaud":3011.56,"xageur":22.758,"XAUGBP":1584.05,"xagaud":37.927,"Copper":3.8791,"usdcnh":6.92465,"gertec30":3262.4,"NatGas":2.235,"OJ":275.76,"SpotCrude":76.624,"SpotBrent":80.372,"Gasoline":2.5412,"usdchf":0.89381,"nzdchf":0.5524,"chfjpy":152.369,"usdx":101.213,"eurx":1043.2,"jpyx":813.9,"XAUCHF":1779.26,"AUDJPY":90.093}

def get_last_line(file_path):
    with open(file_path, 'rb') as file:
        file.seek(-2, SEEK_END)
        while file.read(1) != b'\n':
            file.seek(-2, SEEK_CUR)
        last_line = file.readline().decode().strip()
        return last_line

def parse_price_info(price_info):
    data = ujson.loads(price_info)
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
            # trigger an alert (e.g. send an email or SMS message)
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text='Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}'"
                session.get(url).json()
                print(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}')
                print("Target price reached. Stopping the script...")
                break
            elif alert_type == 'above' and math.isclose(prices[currency], target_price, rel_tol=1e-5):
                # trigger an alert (e.g. send an email or SMS message)
                url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text='Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}'"
                session.get(url).json()
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
