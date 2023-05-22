import random
import time
import httplib
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import MySQLdb

# Database connection details
db_host = 'localhost'
db_user = 'root'
db_password = 'Gsw@1924'
db_name = 'esamproject'

voltage1 = 0
current1 = 0
energy1 = 0
voltage2 = 0
current2 = 0
energy2 = 0
voltage3 = 0
current3 = 0
energy3 = 0
relay_state1 = None
relay_state2 = None
relay_state3 = None
relay_id = None
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global voltage1, current1, energy1, voltage2, current2, energy2, voltage3, current3, energy3, relay_state1, relay_state2, relay_state3, relay_id
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        json_data = json.loads(data)
        print(json_data)  # Process the received JSON data as desired
        if json_data.get('id') == 'load1':
            voltage1 = json_data.get('voltage')
            current1 = json_data.get('current')
            energy1 = json_data.get('power')
        elif json_data.get('id') == 'load2':
            voltage2 = json_data.get('voltage')
            current2 = json_data.get('current')
            energy2 = json_data.get('power')
        elif json_data.get('id') == 'load3':
            voltage3 = json_data.get('voltage')
            current3 = json_data.get('current')
            energy3 = json_data.get('power')
        elif json_data.get('id') == 'relay1':
            relay_stage = json_data.get('state')
            print(relay_stage)
            relay_id = 'relay1'
            if relay_stage == "ON":
                relay_state1 = 1
            elif relay_stage =="OFF":
                relay_state1 = 0
        elif json_data.get('id') == 'relay2':
            relay_id = 'relay2'
            relay_stage = json_data.get('state')
            print(relay_stage)
            if relay_stage == "ON":
                relay_state2 = 1
            elif relay_stage =="OFF":
                relay_state2 = 0
        elif json_data.get('id') == 'relay3':
            relay_id = 'relay3'
            relay_stage = json_data.get('state')
            print(relay_stage)
            if relay_stage == "ON":
                relay_state3 = 1
            elif relay_stage =="OFF":
                relay_state3 = 0
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        global relay_state1, relay_state2, relay_state3, relay_id
        if self.path == '/endpoint/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if relay_id == 'relay1':
                response_data = {'id' : 'relay1', 'state': relay_state1}
            elif relay_id == 'relay2':
                response_data = {'id' : 'relay2', 'state': relay_state2}
            elif relay_id == 'relay3':
                response_data = {'id' : 'relay3', 'state': relay_state3}
            print(response_data)
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run_server():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server on port 5000...')
    httpd.serve_forever()

def send_data():
    global voltage1, current1, energy1, voltage2, current2, energy2, voltage3, current3, energy3
    while True:
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

        time.sleep(1)  # Delay for 5 seconds before sending the next data


if __name__ == '__main__':
    # Start the server in a separate thread
    import threading
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Start sending data
    send_data()
