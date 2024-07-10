import socket
from datetime import datetime
import json

# class RequestIterator:
#     def __init__(self, request_list):
#         self.req = request_list
    
#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         try:
#             value = self.req[self.index]
#             print(value)
#             return value
#         except StopIteration:
#             return

# def RecievedMessage(req):
#     msg = json.loads(req)
#     return msg

# class BaseRequestHandler:
#     def handle_request():
#         print("Base class called")
    
# class GetRequestHandler(BaseRequestHandler):
#     def handle_request():
#         print("Get class called")

# class PostRequestHandler(BaseRequestHandler):
#     def handle_request():
#         print("Post class called")


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
                client.send('Thank you for connecting'.encode())
                request = client.recv(1024).decode()
                print(request)
        except KeyboardInterrupt:
            print("\nServer is shutting down...")
