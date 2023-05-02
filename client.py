import json
import requests

# Send the two variables to the server
url = 'http://192.168.43.67:8000'  # Change this to the address of your server
data = {'var1': 1.0, 'var2': 2.0}
response = requests.post(url, json=data)

# Parse the response JSON
result = json.loads(response.text)
result1 = result.get('result1')
result2 = result.get('result2')
print(f"Received results: {result1}, {result2}")