import socket
import json
import asyncio

dummy_requests = [
    {
        "Username": "luca",
        "Method": "GET",
        "Access": ""
    }, 
    {
        "Username": "ye",
        "Method": "GET",
        "Access": ""
    },
    {
        "Username": "luca",
        "Method": "POST", 
        "Content": "It's a lot of reasons not to speak at all, You probably wonder if I bleed at all",
        "Access": ""
    },
    {
        "Username": "jhon",
        "Method": "POST",
        "Content": "Hi everyone!",
        "Access": ""
    },
    {
        "Username": "sandy",
        "Method": "GET",
        "Access": ""
    }
]

class Singleton(type):
    instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instances[cls]

class ClientContextManager(metaclass=Singleton):
    def __enter__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket successfully created\n")
        return self.client
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()

with ClientContextManager() as s:
    try:
        s.connect(("127.0.0.1", 5000)) 
        msg = json.dumps(dummy_requests)
        s.send(msg.encode())
        while True:
            data = s.recv(1024).decode()
            print(f"{data}")
            if data.endswith("Done"):
                break
    except socket.error as err:
        print("Can't connnect to the server %s" %(err))
    except KeyboardInterrupt:
        print("\nSession Closed.")