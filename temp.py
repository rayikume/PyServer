import socket
from datetime import datetime
import json

# Decorator that print that logs each incoming request.
def log_request(func):
    def wrapper(*args, **kwargs):
        current_time = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        result = func(*args, **kwargs)
        print(f"Recieved a request at {current_time}.")
        return result
    return wrapper

# Decorator that checks if a request is authorized.
def authorize_request(func):
    def wrapper(*args, **kwargs):
        request = func(*args, **kwargs)
        if request["Username"] == "luca":
            request["Access"] = True
            return request
        else:
            request["Access"] = False
            return request
    return wrapper

def response_generator(status, response):
    response = {
        "Status": status,
        "Response": response
    }
    yield response

def streaming_response_generator(response, chunk_size=1024):
    for i in range(0, len(response), chunk_size):
        yield response[i:i + chunk_size]

# Iterator protocol to manage multiple requests.
class RequestIterator:
    def __init__(self, request_list):
        self.req = request_list
        self.index = 0
    
    def __iter__(self):
        return self
    
    @log_request
    @authorize_request
    def __next__(self):
        if self.index < len(self.req):
            value = self.req[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

class BaseRequestHandler:
    def handle_request(self, request):
        if request.get("Access") == True:
            if request.get("Method") == "GET":
                return GetRequestHandler().handle_request()
            if request.get("Method") == "POST":
                return PostRequestHandler().handle_request()
        else:
            return "Access Denied"
    
class GetRequestHandler(BaseRequestHandler):
    def handle_request(self):
        response = response_generator(200, "imagine you got what you asked for")
        return response
class PostRequestHandler(BaseRequestHandler):
    def handle_request(self):
        response = response_generator(200, "successful submission")
        return response

# Context manager that handles server's operation
class ServerContextManager:
    def __enter__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 5000))
        self.server.listen(5)
        return self.server
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.server.close()

with ServerContextManager() as server:
    print("\nServer is listening...\n")
    try:
        while True:
            print("----------------------------------------------------------------------------------------------")
            client, client_address = server.accept()
            print(f"Connected with {client_address}\n")
            request = client.recv(1024).decode()
            objson = json.loads(request)
            objIteration = RequestIterator(objson)
            responses = []
            for x in objIteration:
                if x["Access"] == True:
                    response = BaseRequestHandler().handle_request(x)
                    responses.extend(response)
                else:
                    responses.append("Access Denied.")
            for x in responses:
                serial = json.dumps(x)
                client.send(serial.encode())
            client.send("DONE".encode())
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
