from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def handle_data():
    data = request.get_json(force=True)
    print(data)  # Process the received JSON data as desired
    return 'Data received successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)