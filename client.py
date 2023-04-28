import json
import urequests

# Send the two variables to the server
url = 'http://localhost:8000'
data = {'var1': 1.0, 'var2': 2.0}
response = urequests.post(url, json=data)

# Parse the response JSON
result = json.loads(response.text)
result1 = result['result1']
result2 = result['result2']
print(f"Received results: {result1}, {result2}")
