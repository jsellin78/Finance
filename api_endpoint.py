#! /usr/bin/env python3

import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

#Instead of saving the contents of the value coming into the http server to a file, as in server2.py we store the data in the servers memory and we can acess the endpoint with a curl request 

COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"

class S(BaseHTTPRequestHandler):
    
    def _set_response(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        
    def do_log(self, method):
        logging.info(f"{COLOR}[{self.address_string()}]{RESET_COLOR} {method} {self.path}")
    
    def do_GET(self): #Get when we make a curl request to the server to get the data that is stored there. 
        self.do_log("GET")
        if self.path == '/posts':
        # Check if there is data stored in the server's memory
            if hasattr(self.server, 'value'):
                self._set_response('application/json')
           
                post_values = self.server.value   # Get the data from the server's memory
                self.wfile.write(json.dumps(post_values).encode('utf-8')) # # Send the data as a JSON response
            else:
                self.send_error(404, 'No data found')
        else:
            pass                
    
    def do_POST(self): #Post defining the data thats coming in to the http server 
        self.do_log("POST")
        if self.path == '/posts': #endpoint of the api 
            self._set_response('application/json') # Set the response headers
            content_length = self.headers.get('Content-Length')  # Get the length of the incoming POST data
            content_length = 0 if content_length is None else int(content_length) 
            # Read the POST data and parse it as JSON
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            print(json.dumps(data, indent=4))
            time = data.get('Time')
            us = data.get('us30')
            nas = data.get('nas100')
            ger = data.get('ger40')
            gertec = data.get('gertec30')
            uk = data.get('uk100')
            jpn = data.get('jpn225')            
            cn = data.get('cn50')
            brent = data.get('SpotBrent')
            crude = data.get('SpotCrude')
            gasoline = data.get('Gasoline')
            usdjpy = data.get('usdjpy')
            usdcnh = data.get('usdcnh')
            gbpjpy = data.get('gbpjpy')
            gbpusd = data.get('gbpusd')
            cadjpy = data.get('cadjpy')
            gbpnzd = data.get('gbpnzd')
            usdcad = data.get('usdcad')
            eurusd = data.get('eurusd')
            eurchf = data.get('eurchf')
            euraud = data.get('euraud')
            eurgbp = data.get('eurgbp')
            eurjpy = data.get('eurjpy')
            eurcad = data.get('eurcad')
            nzdusd = data.get('nzdusd')
            audnzd = data.get('audnzd')
            audusd = data.get('audusd') 
            btcusd = data.get('btcusd')
            sugar = data.get('sugar')
            gbpaud = data.get('gbpaud')
            gbpcad = data.get('gbpcad')
            eurnzd = data.get('eurnzd')
            audcad = data.get('audcad')
            nzdcad = data.get('nzdcad')
            coffe = data.get('coffe')
            cotton = data.get('cotton')
            cocoa = data.get('cocoa')
            wheat = data.get('wheat')
            soybeans = data.get('soybeans')
            rghrice = data.get('rghrice')
            xauusd = data.get('xauusd')
            xauaud = data.get('xauaud')
            xauchf = data.get('xauchf')

            post_values = {
                'time': time,
                'us': us,
                'nas': nas,
                'ger': ger,
                'gertec': gertec,
                'uk': uk,
                'jpn': jpn,
                'cn': cn, 
                'brent': brent, 
                'crude': crude, 
                'gasoline': gasoline,
                'usdjpy': usdjpy, 
                'usdcnh': usdcnh,
                'gbpjpy': gbpjpy, 
                'gbpusd': gbpusd, 
                'cadjpy': cadjpy,  
                'gbpnzd': gbpnzd, 
                'usdcad': usdcad, 
                'eurusd': eurusd, 
                'eurchf': eurchf, 
                'euraud': euraud, 
                'eurgbp': eurgbp, 
                'eurjpy': eurjpy, 
                'eurcad': eurcad, 
                'nzdusd': nzdusd, 
                'audnzd': audnzd, 
                'audusd': audusd, 
                'btcusd': btcusd, 
                'sugar': sugar, 
                'gbpaud': gbpaud, 
                'gbpcad': gbpcad, 
                'eurnzd': eurnzd, 
                'audcad': audcad, 
                'nzdcad': nzdcad, 
                'coffe': coffe, 
                'cotton': cotton, 
                'cocoa': cocoa, 
                'wheat': wheat, 
                'soybeans': soybeans, 
                'rghrice': rghrice, 
                'xauusd': xauusd, 
                'xauaud': xauaud, 
                'xauchf': xauchf
                }

            self.server.value = post_values #store the data in the server's memory
            self.send_response(200) #  # Send a response indicating that the update was successful
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        else:
            # Handle other POST requests here
            pass
    
    def do_PUT(self):
        self.do_log("PUT")

    def do_DELETE(self):
        self.do_log("DELETE")


def run(address, port, server_class=HTTPServer, handler_class=S):
    logging.basicConfig(level=logging.INFO)
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:\n" + sys.argv[0] + " [address] [port]")
        sys.exit(1)
    run(sys.argv[1], int(sys.argv[2]))
