import socket

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket successfully created")
except socket.error as err: 
    print ("socket creation failed with error %s" %(err))
 
try:
    s.connect(("127.0.0.1", 5000)) 
    s.send('A'.encode())
    print (s.recv(1024).decode())
except socket.error as err:
    print("Can't connnect to the server %s" %(err))
finally:
    s.close() 