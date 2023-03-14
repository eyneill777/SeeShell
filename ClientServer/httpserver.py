from socket import *

# start server on port 12000 and begin listening
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
#accepts connection, checks if a GET or PUT, and then executes accordingly
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        request = connectionSocket.recv(1024).decode().split(' ')
        # reject if the request is not a GET or PUT
        if request[0] not in ['GET','PUT']:
            connectionSocket.send(b"ERROR: Method not implemented")
        # open file with name of requested file, read in bytes, and store in file variable
        elif request[0] == 'GET':
            try:
                f = open(request[1][1:],'rb')
                file = f.read()
                f.close()
                # send http response code + file
                connectionSocket.send(b"HTTP/1.0 200 OK\r\n\r\n" + file)
            except FileNotFoundError:
                connectionSocket.send(b"HTTP/1.0 Error 404: File not found\r\n\r\n")
        #recieve sent file in 1 megabyte increments
        elif request[0] == 'PUT':
            totalResponse = b''
            while True:
                response = connectionSocket.recv(1024)
                if not response:
                    break
                totalResponse += response
            #open file with same name as sent file
            #write final transmitted data to file
            f = open(request[1][1:], 'wb')
            f.write(totalResponse)
            f.close()
            #send http response code
            connectionSocket.send(b"HTTP/1.0 200 OK: File created\r\n\r\n")
        connectionSocket.close()
    except KeyboardInterrupt:
        serverSocket.close()
        break
