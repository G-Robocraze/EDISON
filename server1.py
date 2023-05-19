from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        json_data = json.loads(data)
        print(json_data)  # Process the received JSON data as desired

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Data received successfully')

def run():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 5000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
