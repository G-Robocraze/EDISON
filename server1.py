import random
import time
import httplib
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

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
priority_list = []  # Priority list to be updated from Flask server
energy_limit = 1000  # Set your desired energy limit here

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global voltage1, current1, energy1, voltage2, current2, energy2, voltage3, current3, energy3, relay_state1, relay_state2, relay_state3, relay_id, priority_list
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
            elif relay_stage == "OFF":
                relay_state1 = 0
        elif json_data.get('id') == 'relay2':
            relay_id = 'relay2'
            relay_stage = json_data.get('state')
            print(relay_stage)
            if relay_stage == "ON":
                relay_state2 = 1
            elif relay_stage == "OFF":
                relay_state2 = 0
        elif json_data.get('id') == 'relay3':
            relay_id = 'relay3'
            relay_stage = json_data.get('state')
            print(relay_stage)
            if relay_stage == "ON":
                relay_state3 = 1
            elif relay_stage == "OFF":
                relay_state3 = 0
        elif json_data.get('id') == 'priority_list':
            next_priorities = []
            for i in range(1, len(json_data)):
                priority_key = 'priority_' + str(i)
                priority_load = json_data.get(priority_key)
                if priority_load:
                    next_priorities.append(priority_load)
            print("Next priorities:", next_priorities)
            priority_list.extend(next_priorities)
            print("Updated priority list:", priority_list)


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
                response_data = {'id': 'relay1', 'state': relay_state1}
            elif relay_id == 'relay2':
                response_data = {'id': 'relay2', 'state': relay_state2}
            elif relay_id == 'relay3':
                response_data = {'id': 'relay3', 'state': relay_state3}
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

        time.sleep(1)  # Delay for 1 second before sending the next data

def manage_loads():
    global energy_limit, priority_list, relay_state1, relay_state2, relay_state3
    total_energy = energy1 + energy2 + energy3

    def cut_load(index):
        load_id = priority_list[index]

        if load_id == 'load1' and relay_state1 == 1:
            relay_state1 = 0
            print("Turning off load1 (priority {})".format(index + 1))
        elif load_id == 'load2' and relay_state2 == 1:
            relay_state2 = 0
            print("Turning off load2 (priority {})".format(index + 1))
        elif load_id == 'load3' and relay_state3 == 1:
            relay_state3 = 0
            print("Turning off load3 (priority {})".format(index + 1))

    def check_loads(current_index):
        if current_index < len(priority_list):
            cut_load(current_index)

            # Check if total energy gradually decreases below the limit
            while energy1 + energy2 + energy3 > energy_limit:
                time.sleep(1)  # Wait for 1 second before checking again

            # Check the next priority load
            check_loads(current_index + 1)

    if total_energy > energy_limit:
        # Start checking the priority loads
        check_loads(0)

    time.sleep(1)  # Delay for 1 second before checking again
    manage_loads()  # Recursively call the function to continue monitoring and managing the loads


if __name__ == '__main__':
    # Start the server in a separate thread
    import threading
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Start sending data
    send_data_thread = threading.Thread(target=send_data)
    send_data_thread.daemon = True
    send_data_thread.start()

    # Start load management
    manage_loads_thread = threading.Thread(target=manage_loads)
    manage_loads_thread.daemon = True
    manage_loads_thread.start()

    while True:
        time.sleep(1)
