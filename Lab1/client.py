__author__ = 'Jonas Andersson'
# !/usr/bin/python
from socket import *
import threading
import server
import json

# Global State
host = "127.0.0.1"
port = 5555
request = {'request': 'GET /helloWorld.html'}


def client_connector():
    print('Client Started')
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    reply = send_data(sock, request)
    print(reply['status_code'] + reply['status_message'])
    sock.close()


def send_data(sock, raw_data):
    reply = None
    data = json.dumps(raw_data)
    if sock:
        sock.send(data.encode())
        print("Data sent")
        raw_reply = sock.recv(1024).decode('utf-8')
        reply = json.loads(raw_reply)
    return reply

if __name__ == '__main__':
    client_connector()

