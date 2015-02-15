__author__ = 'Jonas Andersson'
#!/usr/bin/python
from socket import *

#Global State
host = "127.0.0.1"
port = 5555
serving = True


def serve_forever():
    print("Server Starting")
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    while serving:
        try:
            print('server while loop')
            socket_connection, addr = s.accept()
            print('Got connection from', addr)
            socket_connection.send('Thank you for connecting'.encode())
            socket_connection.close()
        except:
            socket_connection.close()

if __name__ == '__main__':
    serve_forever()