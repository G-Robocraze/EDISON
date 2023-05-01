import network
import machine
import socket

# Set up Wi-Fi connection
ssid = "AndroidAP"
password = "gsw@1234"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    pass

# Define server function
def http_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 80))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello World!"
        conn.send(response.encode())
        conn.close()

# Run the server function
http_server()