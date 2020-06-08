'''
  @author simransingh
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/start":
            self._set_headers()
            self.wfile.write(json.dumps({'method': 'GET', 'hello': 'world', 'received': 'ok'}).encode('utf8'))

    def do_POST(self):
        if self.path == "/start":
            self._set_headers()
            self.wfile.write(json.dumps({'method': 'POST', 'hello': 'world', 'received': 'ok'}).encode('utf8'))

server_address = ('localhost', 8888)
httpd = HTTPServer(server_address, Server)

print(f"Starting httpd server on {'localhost'}:{8888}")
httpd.serve_forever()

