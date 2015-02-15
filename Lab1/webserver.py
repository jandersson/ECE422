from socket import *
# JSON handles serializing and de-serializing data sent over socket
import json

# Global State
address = "127.0.0.1"
port = 5555
socket_tuple = (address, port)
serving = True

# Python naming convention is to use underscores instead of camel case
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(socket_tuple)
server_socket.listen(1)

while serving:
    print('Starting Server')
    # Set up a new connection from the client using accept
    connection, address = server_socket.accept()
    print('Server got connection from ', address)
    try:
        # Receives the request message from the client
        raw_data = connection.read().decode()
        if not raw_data:
            break
        # May need to change this to do json.loads(raw_data)
        message = json.loads(raw_data)
        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        # for example "GET /HelloWorld.html HTTP/1.1" we take only "/HelloWorld.html HTTP/1.1
        # so use some method to split the "GET" from "GET /HelloWorld.html HTTP/1.1"

        filename = message['request']#Fill in start  #Fill in end
        # Because the extracted path of the HTTP request includes
        # a character '/', we read the path from the second character i.e."HelloWorld.html"
        # Using string Operations you know to remove first character
        f = open(filename[1:])
        with open(filename[1:], 'r') as f:
            outputdata = f.read()

        # Send the HTTP response header line to the connection socket
        # We are using "b" here because, we send bytes not strings.
        connection.send(b"HTTP/1.1 200 OK\r\n\r\n")


        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connection.send(outputdata[i])
        connection.send(b"\r\n")

        # Close the client connection socket
        connection.close()

    except IOError:
        print('IOError')
        # Send HTTP response message for file not found to client socket. You have studied error messages in chapter 2
        # Fill in start

        #Fill in end

        # Close the client connection socket
        #Fill in start #Fill in end

server_socket.close()

