import socket
import json

dummy_requests = [
    {
        "Username": "luca",
        "Method": "GET"
    }, 
    {
        "Username": "ye",
        "Method": "GET"
    },
    {
        "Username": "luca",
        "Method": "POST", 
        "Content": "It's a lot of reasons not to speak at all, You probably wonder if I bleed at all"
    },
    {
        "Username": "jhon",
        "Method": "POST",
        "Content": "Hi everyone!"
    },
    {
        "Username": "sandy",
        "Method": "GET"
    }
]

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
except socket.error as err: 
    print ("socket creation failed with error %s" %(err))
 
try:
    s.connect(("127.0.0.1", 5000)) 
    msg = json.dumps(dummy_requests)
    s.send(msg.encode())
    print (s.recv(1024).decode())
except socket.error as err:
    print("Can't connnect to the server %s" %(err))
finally:
    s.close() 