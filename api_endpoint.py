#! /usr/bin/env python3

import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# curl http://192.168.1.220:2046/4hour/USDCHF/low 
# curl http://192.168.1.220:2046/4hour/GBPJPY/high 
# curl http://192.168.1.220:2046/4hour/GBPJPY #Full json response 


COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"


class S(BaseHTTPRequestHandler):
    
    def _set_response(self, content_type='text/html'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        
    def do_log(self, method):
        logging.info(f"{COLOR}[{self.address_string()}]{RESET_COLOR} {method} {self.path}")
   
                        
    def do_GET(self):
        self.do_log("GET")
        if self.path.startswith('/4hour/'):
            # Extract the currency pair from the URL
            url_parts = self.path.split('/')
            currency_pair = url_parts[2] # /4hour/parts[2]

            # If a specific value is requested, extract it from the URL
            value = None
            if len(url_parts) == 4:
                value = url_parts[3] #/4hour/currency/parts[3]

            # Check if there is data stored in the server's memory
            if hasattr(self.server, 'value'):
                # Filter the data based on the currency pair
                filtered_data = [data for data in self.server.value if data['currency'] == currency_pair]
                if filtered_data:
                    # If a specific value is requested, extract it from the data
                    if value:
                        result = [data[value] for data in filtered_data]
                        # Remove the brackets and hash symbol from the result
                        result = str(result[0]).replace('[', '').replace(']', '').replace('#', '').replace('"', '')
                    else:
                        result = filtered_data
                    # Set the response headers
                    self._set_response('application/json')
                    # Send the result as a JSON response
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    # If there is no data for the given currency pair, send a 404 response
                    self.send_error(404, f'No data found for currency pair {currency_pair}')
            else:
                # If there is no data, send a 404 response
                self.send_error(404, 'No data found')
        else:
            # Handle other GET requests here
            pass
    
    def do_POST(self): #Post defining the data thats coming in to the http server 
        self.do_log("POST")
        if self.path == '/4hour': #endpoint of the api 
            # Set the response headers
            self._set_response('application/json')
            # Get the length of the incoming POST data
            content_length = self.headers.get('Content-Length')
            content_length = 0 if content_length is None else int(content_length) 
            # Read the POST data and parse it as JSON
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            print(type(data))

            post_values_list = []
            for post in data:
               time = post.get('time')
               currency = post.get('Currency')
               prevclose = post.get('PrevClose')
               open_ = post.get('Open')
               high = post.get('High')
               low = post.get('Low')
               close = post.get('Close')

               post_values = {
                   'time': time,
                   'currency': currency,
                   'prevclose': prevclose,
                   'open': open_,
                   'high': high,
                   'low': low,
                   'close': close,
               }
               post_values_list.append(post_values)

            print(json.dumps(post_values_list, indent=4))
   
            self.server.value = post_values_list # # Store the list of dictionaries in the server's memory
            self.send_response(200) # # Send a response indicating that the update was successful
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




