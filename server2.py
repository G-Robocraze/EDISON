import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class Server2Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        json_data = self.rfile.read(content_length)
        data = json.loads(json_data)
        value1 = data.get('value1')
        value2 = data.get('value2')
        value3 = data.get('value3')
        print 'Received values from ESP32:', value1, value2, value3
        response = {'value1': value1, 'value2': value2, 'value3': value3}
        response_json = json.dumps(response)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_json)

server2 = HTTPServer(('', 8081), Server2Handler)
print 'Starting Server 2...'
server2.serve_forever()
