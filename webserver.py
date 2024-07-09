import socket
from datetime import datetime

def log_request(func):
    def wrapper(*args, **kwargs):
        current_time = datetime.now()
        req = func(*args, **kwargs)
        content = f"Recieved a request at {current_time} and its content {req}"
        return content
    return wrapper

@log_request
def RecievedMessage(req):
    return req

s = socket.socket()
port = 5000
s.bind(('', port))         
s.listen(5)     
print ("server is listening...")

try:
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        c.send('Thank you for connecting'.encode())
        message = c.recv(1024).decode()
        print(RecievedMessage(message))
except KeyboardInterrupt:
    print("\nServer is shutting down...")
finally:
    s.close()