#! /usr/bin/env python3

import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

# curl http://192.168.1.220:2046/4hour/USDCHF/low 
# curl http://192.168.1.220:2046/4hour/GBPJPY/high 
# curl http://192.168.1.220:2046/4hour/GBPJPY #Full json response 

COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"


class S(BaseHTTPRequestHandler):
    
    def _set_response(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', 'content_type')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()
        
        if content_type == 'application/json':
           self.wfile.write(b'\n')
        
    def do_log(self, method):
        logging.info(f"{COLOR}[{self.address_string()}]{RESET_COLOR} {method} {self.path}")
   
            

    def do_GET(self):
        self.do_log("GET")
        if self.path.startswith('/4hour/'):
            url_parts = self.path.split('/')
            currency_pair = url_parts[2]

            value = None
            if len(url_parts) == 4:
                value = url_parts[3]

            if hasattr(self.server, 'value'):
                filtered_data = [data for data in self.server.value if data['currency'] == currency_pair]
                if filtered_data:
                    if value:
                        result = str(filtered_data[0][value]).replace('\#', '').replace('"', '').replace('#', '')
                    else:
                        result = filtered_data
                        for res in result:
                            for k, v in res.items():
                                if isinstance(v, str):
                                    res[k] = v.strip('#"')

                    self._set_response('application/json')
                    if 'jq' in self.headers.get('User-Agent', ''):
                        # Use jq to process the JSON data
                        cmd = f'echo \'{json.dumps(result)}\' | jq -c'
                        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                        out, _ = p.communicate()
                        self.wfile.write(out)
                    else:
                        self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    self.send_error(404, f'No data found for currency pair {currency_pair}')
            else:
                self.send_error(404, 'No data found')
        else:
            pass
     
    def do_POST(self): #Defining the data thats coming in to the http server 
        self.do_log("POST")
        if self.path == '/4hour': #endpoint of the api 
            # Set the response headers
            self._set_response('application/json')
            content_length = self.headers.get('Content-Length')
            content_length = 0 if content_length is None else int(content_length) 
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            logging.info(f"Received data: {json.dumps(data)}")
            print(type(data))

            post_values_list = []
            for post in data:
               time = post.get('Time')
               currency = str(post.get('Currency')).replace('#', '')
               prevclose = str(post.get('PrevClose')).replace('#', '')
               open_ = str(post.get('Open')).replace('#', '')
               high = str(post.get('High')).replace('#', '')
               low = str(post.get('Low')).replace('#', '')
               close = str(post.get('Close')).replace('#', '')

               post_values = {
                   'time': time,
                   'currency': currency,
                   'prevclose': prevclose,
                   'open': open_,
                   'high': high,
                   'low': low,
                   'close': close
               }
               post_values_list.append(post_values)
            logging.info(f"Parsed data: {json.dumps(post_values_list, indent=4)}")
            print(json.dumps(post_values_list, indent=4))
            self.server.value = post_values_list 
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        else:
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




