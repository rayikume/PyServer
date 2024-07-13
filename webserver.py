import socket
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, MagicMock
import json
import asyncio
import random

# Decorator that logs each incoming request.
def log_request(func):
    async def wrapper(*args, **kwargs):
        current_time = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        result = await func(*args, **kwargs)
        print(f"Received a request at {current_time}.")
        return result
    return wrapper

# Decorator that checks if a request is authorized.
def authorize_request(func):
    async def wrapper(*args, **kwargs):
        request = await func(*args, **kwargs)
        if request.get("Username", "").lower() == "luca":
            request["Access"] = True
        else:
            request["Access"] = False
        return request
    return wrapper

def response_generator(response, method):
    res = f"[{datetime.now().strftime('%d/%m/%Y %I %p')}]: Received /{method} Response: {response}"
    yield res

async def streaming_response_generator(body_chunks):
    for chunk in body_chunks:
        await asyncio.sleep(random.randrange(1, 3))
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

class AsyncRequestIterator:
    def __init__(self, request_list):
        self.req = request_list
        self.index = 0

    def __aiter__(self):
        return self

    @log_request
    @authorize_request
    async def __anext__(self):
        if self.index < len(self.req):
            value = self.req[self.index]
            self.index += 1
            return value
        else:
            raise StopAsyncIteration

class BaseRequestHandler:
    async def handle_request(self, request):
        if request.get("Access") == True:
            if request.get("Method") == "GET":
                return  await GetRequestHandler().handle_request()
            if request.get("Method") == "POST":
                return  await PostRequestHandler().handle_request()
        else:
            return ["Access Denied"]

class GetRequestHandler(BaseRequestHandler):
    async def handle_request(self):
        response = response_generator("Imagine you got what you asked for", "GET")
        return response

class PostRequestHandler(BaseRequestHandler):
    async def handle_request(self):
        response = response_generator("Successful submission!", "POST")
        return response
    
async def async_request_handler(client):
    try:
        request = await asyncio.wait_for(asyncio.to_thread(client.recv, 1024), timeout=5.0)
        request = request.decode()
        objson = json.loads(request)
        objIteration = AsyncRequestIterator(objson)
        responses = []
        async for x in objIteration:
            response = await BaseRequestHandler().handle_request(x)
            responses.extend(response)
        stream = streaming_response_generator(responses)
        async for part in stream:
            await asyncio.to_thread(client.send, f"{part}".encode())
        await asyncio.to_thread(client.send, "\nDone".encode())
        client.close()
    except asyncio.TimeoutError:
        print("Request timed out.")
        client.close()
    
async def stop_server_after_delay(delay):
    await asyncio.sleep(delay)
    return False

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

async def main():
    loop = True
    with ServerContextManager() as server:
        print("\nServer is listening...\n")
        while loop == True:
            print("----------------------------------------------------------------------------------------------")
            client, client_address = await asyncio.to_thread(server.accept)
            print(f"Connected with {client_address}\n")
            asyncio.create_task(async_request_handler(client))
            loop = await stop_server_after_delay(15)
        print("\nServer is shutting down...\n")

asyncio.run(main())