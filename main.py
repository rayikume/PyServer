import socket
import json

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

class ClientContextManager:
    def __enter__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket successfully created")
        return self.client
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()

with ClientContextManager() as s:
    complete_data = ""
    try:
        s.connect(("127.0.0.1", 5000)) 
        msg = json.dumps(dummy_requests)
        s.send(msg.encode())
        while True:
            data = s.recv(1024).decode()
            if data.endswith("DONE"):
                complete_data += data[:-4]
                break
            complete_data += data
        print("Received data:", complete_data)
    except socket.error as err:
        print("Can't connnect to the server %s" %(err))
    except KeyboardInterrupt:
        print("\nSession Closed.")