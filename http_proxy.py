import os
import sys
import socket
import thread
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # get port from arguments
    if (len(sys.argv)<3):
        port = 8080
        print("Defaulting to port 8080")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])

    print("HTTP Proxy started on %s:%s \n" % (host, port))
    
    try:
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # associate the socket to host and port
        s.bind((host, port))
        # listen on this socket
        s.listen(25)
    except socket.error, (value, message):
        if s:
            s.close()
        print("Could not open socket: %s \n" % (message))
        sys.exit(1)

    # get the connection from client
    while 1:
        conn, client_addr = s.accept()
        # create a thread to handle request via HTTP
        thread.start_new_thread(proxy_thread, (conn, client_addr))
    s.close()

# extracts webserver host and port from url
def grab_server_port(url):
    host = ""
    tmp_url = ""
    port = -1

    http_index = url.find("://")
    if (http_index == -1):
        tmp_url = url
    else:
        tmp_url = url[(http_index + 3):]

    host_index = tmp_url.find("/")
    port_index = tmp_url.find(":")
   
    if host_index == -1:
        host_index = len(tmp_url)
    
    # if port is not found, default to 80, else set port
    if (port_index==-1 or host_index < port_index):
        host = tmp_url[:host_index]
        port = 80
    else:
        host = tmp_url[:port_index]
        port = int((tmp_url[(port_index + 1):])[:host_index - port_index - 1])

    return host, port


# create MIT proxy connection
def proxy_connection_to_server(conn, host, port, req):
    try:
        # create socket for connect to webserver
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("Connected to %s:%s \n" % (host, port))

        # forward the request from proxy to the webserver
        s.send(req)
        print("Forwarding request to %s:%s \n" % (host, port))
        logger.info("Forwarding request to %s:%s \n" % (host, port))

        while 1:
            # get response
            response = s.recv(1000000)
            
            if (len(response) > 0):
                # forward the response to the browser
                conn.send(response)
            else:
                break

        s.close()
        conn.close()

    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()

        print "Resetting peer"
        sys.exit(1)


# Thread to handle request for proxy server
def proxy_thread(conn, client_addr):
    # get the request from client
    request = conn.recv(1000000)

    logger.info(request)

    # get the first line of request headers
    line = request.split('\n')[0]

    # get url 
    first_request_header_line = line.split(" ")
    url = first_request_header_line[1]

    # filter only the HTTP calls that are relevant to PEARS search
    if "http://localhost:5000" not in url:
        print "Peer Reset, not relevant to PEARS"
        sys.exit(1)

    # grab http host and port from url
    host, port = grab_server_port(url)
    proxy_connection_to_server(conn, host, port, request)


if __name__ == '__main__':
    # create a file handler
    handler = logging.FileHandler('analyzer.log')
    handler.setLevel(logging.INFO)

    # create a logging format

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger

    logger.addHandler(handler)
    main()