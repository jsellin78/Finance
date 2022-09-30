#! /usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sys
import codecs
import subprocess
import json
import html

COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_log(self, method):
        content_length = self.headers['Content-Length']
        content_length = 0 if (content_length is None) else int(content_length)
        post_data = self.rfile.read(content_length)
        post = post_data.decode('utf-8')
        post1 = post.strip("\'")
        with open("/tmp/btcusd.txt",'a', encoding='utf-8') as fd: #Put all incoming data from the http-server in a txt file Line by Line always for further proccessing.
              fd.write(str(post1 + '\n')) #When http server recives data this Command notices it, and runs btcusd1.sh  # inotifywait -m -e close_write /tmp/btcusd.txt --format --quiet | while read -r dir; do /files/ifvalueminute/btcusd1.sh ENTER; sleep 2; /files/ifvalueminute/ifvaluebtcusdminute.sh; done
              print(str(post1))
              self._set_response()

    def do_GET(self):
        self.do_log("GET")

    def do_POST(self):
        self.do_log("POST")

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
