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

def response_generator(req, method):
    try:
        if method == "GET":
            yield {
                "Status": "200",
                "Response": "You Recieved What You're Looking For!"
            }
        if method == "POST":
            yield {
                "Status": "200",
                "Response": "You're Content is Submitted Successfully!"
            }
    except:
        yield {
            "Status": "404",
            "Response": "Error Generating Response"
        }

def streaming_response_generator():
    pass


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
    def handle_request(self):
        print("Base class called")
    
class GetRequestHandler(BaseRequestHandler):
    def handle_request(self, request):
        response = response_generator(request, "GET")
        response_list = list(response)
        return response_list

class PostRequestHandler(BaseRequestHandler):
    def handle_request(self):
        response = response_generator(request, "POST")
        response_list = list(response)
        return response_list

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
            lista = RequestIterator(objson)
            responses = []
            for x in lista:
                if x.get("Access") == True:
                    if x.get("Method") == "GET":
                        response = GetRequestHandler().handle_request(x)
                    if x.get("Method") == "POST":
                        response = PostRequestHandler().handle_request()
                else:
                    response = "Access Denied"
                responses.append(response)
            
            print(responses)
            
            serialized_responses = json.dumps(responses)
            client.sendall(serialized_responses.encode())
            
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
