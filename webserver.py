import socket
from datetime import datetime
import json

auth = False

def log_request(func):
    def wrapper(*args, **kwargs):
        current_time = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        req = func(*args, **kwargs)
        content = f"Recieved a request at {current_time}."
        return content
    return wrapper

def authorize_request(func):
    def wrapper(*args, **kwargs):
        objJSON = func(*args, **kwargs)
        if (objJSON["Email"] == "kw99@gmail.com"):
            auth = True
            print("Access Granted")
        else:
            auth = False
            print("Access Denied")
        return objJSON
    return wrapper

@log_request
@authorize_request
def RecievedMessage(req):
    msg = json.loads(req)
    return msg

# generate response based on request send
def response_generator(req):
    res = {
        "Type": "GET",
        "Content": "Imagine this is the data you're requested"
    }
    yield res

# yields each attribute in the response
def streaming_response_generator(response):
    for x in response:
        yield x[0]

# handle request (Sycronus)
class RequestIterator:
    def __init__(self, req):
        self.req = req
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            value = self.req[self.index]
            self.index += 1
            return value
        except StopIteration:
            return
        
#handel request (Async)
async def async_request_handler(request_list):
    async for request in request_list:
        async for attribute in request:
            print(attribute)



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