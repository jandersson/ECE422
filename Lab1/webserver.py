from socket import *

# Global State
serving = True
address = "127.0.0.1"
port = 5555
buffer_size = 4096
socket_tuple = (address, port)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(socket_tuple)
server_socket.listen(1)
print('Web Server Running')

def parse(request):
    # Parses the request for requested page
    pass


while serving:
    # Set up a new connection from the client using accept
    connection, conn_address = server_socket.accept()
    print('Server got connection from ', conn_address)
    try:
        # Receives the request message from the client
        raw_data = connection.recv(buffer_size).decode('utf-8')
        if not raw_data:
            break
        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        # for example "GET /HelloWorld.html HTTP/1.1" we take only "/HelloWorld.html HTTP/1.1
        # so use some method to split the "GET" from "GET /HelloWorld.html HTTP/1.1"
        raw_data = raw_data.split()
        print(raw_data[1])

        # Because the extracted path of the HTTP request includes
        # a character '/', we read the path from the second character i.e."HelloWorld.html"
        # Using string Operations you know to remove first character
        filename = raw_data[1]
        f = open(filename[1:])
        with open(filename[1:], 'rb') as f:
            outputdata = f.read()

        # Send the HTTP response header line to the connection socket
        # We are using "b" here because, we send bytes not strings.
        connection.send(b"HTTP/1.1 200 OK\r\n\r\n")

        # Send the content of the requested file to the connection socket
        connection.sendall(outputdata)

        # Close the client connection socket
        connection.close()

    except IOError:
        # Send HTTP response message for file not found to client socket. You have studied error messages in chapter 2
        # Fill in start
        connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        with open("404.html", 'rb') as f:
            outputdata = f.read()
        connection.sendall(outputdata)
        #Fill in end

        # Close the client connection socket
        connection.close()

    except KeyboardInterrupt:
        connection.close()
        serving = False

server_socket.close()

