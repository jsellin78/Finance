import time
import json
import os 
import psutil
import sys 
import socket

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

def price_alert(file_path, currency, target_price, max_run_time, host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Listening on {host}:{port}")
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        start_time = time.time()
        while time.time() - start_time < max_run_time:
            last_line = get_last_line(file_path)
            time_str, prices = parse_price_info(last_line)
            if prices.get(currency) and prices[currency] < target_price:
                
                print(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}')
                conn.sendall(f'Price Alert for {currency}! Current price: {prices[currency]:.5f} is below target price: {target_price:.5f} as of {time_str}'.encode())
            time.sleep(60) # wait for 60 seconds before checking again

if __name__ == '__main__':
    file_path = '/root/tmp/currency.txt'
    currency = str(sys.argv[1])
    target_price = float(sys.argv[2]) 
    max_run_time = 2000  
    host = '127.0.1.1' 
    port = 8080
