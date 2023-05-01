import BaseHTTPServer
import SimpleHTTPServer
import cgi
import json

PORT = 8000

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            data = self.rfile.read(length)
            message = json.loads(data)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(json.dumps(message))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Invalid request')

Handler = MyHandler

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
print "serving at port", PORT
httpd.serve_forever()

# import network
# import machine
# import socket

# # Set up Wi-Fi connection
# ssid = "AndroidAP"
# password = "gsw@1234"
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(ssid, password)
# while not wlan.isconnected():
#     pass

# # Define server function
# def http_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind(('0.0.0.0', 80))
#     s.listen(5)
#     while True:
#         conn, addr = s.accept()
#         request = conn.recv(1024)
#         response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello World!"
#         conn.send(response.encode())
#         conn.close()

# # Run the server function
# http_server()