from flask import Flask, render_template, request
import httplib2
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the message from the form
        message = request.form['message']
        
        # Send a request to Server 2
        http_obj = httplib2.Http()
        url = 'http://192.168.43.67:8081/endpoint'
        data = {'message': message, 'id':'id'}
        headers = {'Content-type': 'application/json'}
        json_data = json.dumps(data)
        response, content = http_obj.request(url, 'POST', body=json_data, headers=headers)
        
        # Display the response from Server 2
        return render_template('index.html',response_message=str(content, 'UTF-8'))
        
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
