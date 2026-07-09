
# UDP socket programming

- In UDP socket programming, the server does not establish a connection with the client. Instead, it listens for incoming datagrams (packets) on a specific port and processes them as they arrive. The server can receive data from any client without needing to establish a connection first.
- There are only limited functions available for UDP socket programming, as it is connectionless. The main functions are:
1. bind() Bind the socket to an address and port (done above).
2. recvfrom() Receive data from the socket. It returns a tuple (data, address). No connection prior required.
3. sendto() Send data to the socket. It requires the data and the address to send to.
4. close() Close the socket when done.
5. settimeout() Set a timeout for blocking socket operations.

``` python
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET: IPv4, SOCK_DGRAM: UDP. for TCP, use SOCK_STREAM.
udp_socket.bind(("127.0.0.1", 2053)) # 2053 port randomly selected.


```

## Binded and free ports
- Binded ports are those that are already in use by another application or service. When a socket is bound to a specific port, it means that the operating system has reserved that port for that particular socket, and no other application can use it until the socket is closed or released.
- Free ports, on the other hand, are those that are not currently in use by any application or service. These ports are available for binding and can be used by new sockets to establish communication. When a socket is created and bound to a free port, it becomes a binded port until the socket is closed or released.

- When using UDP sockets as a server (accepting requests and sending responses), choose a free port and bind it to a port. 
- When using UDP sockets as a client (sending request and accepting responses), use a free port to send data to the server. The client does not need to bind to a specific port, as the operating system will automatically assign a free port for the client socket. No need to bind().


# OTHER POINTS
1. single byte is automatically converted to int. to convert series of bytes use int.frombytes()
2. bytes() function takes an iterable of data and returns a byte object.