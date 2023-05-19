import random
import time
import httplib
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
voltage1 = None
current1 = None
energy1 = None
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global voltage1, current1, energy1
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        json_data = json.loads(data)
        print(json_data)  # Process the received JSON data as desired
        if json_data.get('id') == 'load1':
            voltage1 = json_data.get('voltage')
            current1 = json_data.get('current')
            energy1 = json_data.get('power')
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Data received successfully')

def run_server():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 5000...')
    httpd.serve_forever()

def send_data():
    global voltage1, current1, energy1
    while True:
        # Generate random data
        # voltage1 = random.randint(220, 240)
        # current1 = random.randint(1, 10)
        # energy1 = voltage1 * current1
        voltage2 = random.randint(220, 240)
        current2 = random.randint(1, 10)
        energy2 = voltage2 * current2
        voltage3 = random.randint(220, 240)
        current3 = random.randint(1, 10)
        energy3 = voltage3 * current3

        data = {
            'voltage1': voltage1,
            'current1': current1,
            'energy1': energy1,
            'voltage2': voltage2,
            'current2': current2,
            'energy2': energy2,
            'voltage3': voltage3,
            'current3': current3,
            'energy3': energy3
        }

        # Convert data to JSON format
        json_data = json.dumps(data)

        # Send the data to the server
        conn = httplib.HTTPConnection('192.168.43.244', 5000)
        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/receive_data', json_data, headers)
        response = conn.getresponse()

        if response.status == 200:
            print('Data sent successfully')
        else:
            print('Failed to send data')

        conn.close()

        time.sleep(5)  # Delay for 5 seconds before sending the next data

if __name__ == '__main__':
    # Start the server in a separate thread
    import threading
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Start sending data
    send_data()
