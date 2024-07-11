import socket
from datetime import datetime
import json
import asyncio

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

def response_generator(response, method):
    res = f"[{datetime.now().strftime("%d/%m/%Y %I:%M %p")}]: Recieved /{method} Response: {response}"
    yield res

def streaming_response_generator(body_chunks):
        for chunk in body_chunks:
            yield chunk

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
        response = response_generator("Imagine you got what you asked for", "GET")
        return response
class PostRequestHandler(BaseRequestHandler):
    def handle_request(self):
        response = response_generator("Successful submission!", "POST")
        return response

class Singleton(type):
    instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instances[cls]
    
# Context manager that handles server's operation
class ServerContextManager(metaclass=Singleton):
    def __enter__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 5000))
        self.server.listen(5)
        return self.server
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.server.close()

def test_singleton():
    instance1 = ServerContextManager()
    instance2 = ServerContextManager()
    
    print("Instance 1:", instance1)
    print("Instance 2:", instance2)
    print("Are both instances the same?", instance1 is instance2)

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
            stream = streaming_response_generator(responses)
            for part in stream:
                client.send(f"{part}\n".encode())
                print(part)
            client.send("\nDONE".encode())
            test_singleton()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
