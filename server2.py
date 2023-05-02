import json
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Server2Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        json_data = self.rfile.read(content_length)
        print(type(json_data))
        data = json.loads(json_data.decode('utf-8'))
        message = data.get('value')

        print('Received message from Server 1:', message)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Hello from Server 2'.encode('utf-8'))

server2 = ThreadedHTTPServer(('', 8081), Server2Handler)
print('Starting Server 2...')
server2.serve_forever()