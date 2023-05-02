import http.client
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Server1Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Hello from Server 1'.encode('utf-8'))

        # Send a request to Server 2 on Edison
        http_obj = http.client.HTTPConnection('192.168.43.67', 8081)
        data = {'message': 'Hello from Server 1'}
        headers = {'Content-type': 'application/json'}
        json_data = json.dumps(data)
        http_obj.request('POST', '/endpoint', json_data, headers)
        response = http_obj.getresponse()
        content = response.read().decode('utf-8')
        print(content)

server1 = HTTPServer(('localhost', 8080), Server1Handler)
print('Starting Server 1...')
server1.serve_forever()