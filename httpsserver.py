import random
import time
import httplib
import json

def send_data():
    while True:
        # Generate random data
        voltage1 = random.randint(220, 240)
        current1 = random.randint(1, 10)
        energy1 = voltage1 * current1
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
    send_data()