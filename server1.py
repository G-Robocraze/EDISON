import httplib
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class Server1Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Hello from Server 1')

        # Send a request to Server 2
        conn = httplib.HTTPConnection('http://192.168.43.67', 8081)
        data = {'message': 'Hello from Server 1'}
        headers = {'Content-type': 'application/json'}
        json_data = json.dumps(data)
        conn.request('POST', '/endpoint', json_data, headers)
        response = conn.getresponse()
        print(response.read())
        conn.close()

server1 = HTTPServer(('', 8080), Server1Handler)
print('Starting Server 1...')
server1.serve_forever()
