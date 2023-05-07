import json
from SocketServer import ThreadingMixIn
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Server2Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        json_data = self.rfile.read(content_length)
        data = json.loads(json_data)
        message = data.get('message')
        id = data.get('id')
        print 'Received message from', id, ':', message

        # Forward the message to the esp32
        # Modify the code below to fit the specific requirements of your esp32 communication protocol
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('<IP address of the esp32>', <port number>))
        s.sendall(message)
        s.close()

        response = {'message': 'Hello from Server 2'}
        response_json = json.dumps(response)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_json)

server2 = ThreadedHTTPServer(('', 8081), Server2Handler)
print 'Starting Server 2...'
server2.serve_forever()
