import json
import BaseHTTPServer
import SimpleHTTPServer

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        # Parse the request JSON
        data = json.loads(body)
        var1 = float(data['var1'])
        var2 = float(data['var2'])
        print("Received variables: {var1}, {var2}")

        # Send a response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'result1': var1 + 1.0, 'result2': var2 + 2.0}
        self.wfile.write(json.dumps(response))

# Start the HTTP server
server = BaseHTTPServer.HTTPServer(('', 8000), MyHandler)
print('Server running on localhost:8000...')
server.serve_forever()