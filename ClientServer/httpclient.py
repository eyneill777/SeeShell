import sys

def http_get(host, port_number, filename):
    """
    :param host: host website, or server location that you are requesting a file from
    :param port_number: port number you wish to use for this request
    :param filename: which file you wish to retrieve
    :return: http response message
    """
    import socket
    try:
        # create socket object and connect to the host on the specified port
        getsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        getsocket.connect((host, port_number))
        # build and send a http GET message to the host
        message = "GET /"+filename+" HTTP/1.0\r\nHost:"+host+"\r\n\r\n"
        getsocket.send(message.encode())
        # receive first megabyte of data, and strip the http header off
        response = getsocket.recv(1024).split(b"\r\n\r\n")
        header = response[0].split(b'\r\n')[0].decode()
        # put data from first meg into totalResponse
        totalResponse = response[1]
        # loops and continues receiving data in 1 megabyte increments until there is no more
        while True:
            response = getsocket.recv(1024)
            if not response:
                break
            totalResponse += response
        getsocket.close()
        # writes all data into a file with the same name as the requested file
        f = open(filename, 'wb')
        f.write(totalResponse)
        f.close()
        # return the stripped header from earlier specifying the http response code
        return header
    except ConnectionRefusedError:
        print("connection to host failed")

def http_put(host, port_number, filename):
    """
    :param host: host website, or server location that you are sending a file to
    :param port_number: port number you wish to use for this request
    :param filename: which file you wish to send
    :return: http response message
    """
    import socket
    try:
        # create socket object and connect to the host on the specified port
        putsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        putsocket.connect((host, port_number))
        # build and send a http PUT message to the host
        message = "PUT /" + filename + " HTTP/1.0\r\nHost:" + host + "\r\n\r\n"
        putsocket.send(message.encode())
        # open the file to be sent, in read bytes mode
        f = open(filename, 'rb')
        # send file over in 4 megabyte increments,
        # shutdown sending channel after empty
        while True:
            packet = f.read(4096)
            putsocket.send(packet)
            if not packet:
                putsocket.shutdown(socket.SHUT_WR)
                f.close()
                break
        # receive and return http response
        response = putsocket.recv(1024)
        return response.decode()
    except ConnectionRefusedError:
        print("connection to host failed")

def main(host, port_number, mode, filename):
    """
    :param host: host website, or server location
    :param port_number: port number you wish to use for this request
    :param mode: GET or PUT
    :param filename: file to retrieve or send
    """

    if mode not in ['GET', 'PUT']:
        raise Exception("Syntax is httpclient.py host port_num GET/PUT filename")
    elif mode == 'GET':
        print(http_get(host, int(port_number), filename))
    else:
        print(http_put(host, int(port_number), filename))

# call main function using arguments passed in the command line
main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
