import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    #
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET: IPv4, SOCK_DGRAM: UDP. for TCP, use SOCK_STREAM.
    udp_socket.bind(("127.0.0.1", 2053)) # 2053 port randomly selected.
    

    # In UDP socket programming, there are only limited operations.
    # 1. bind() Bind the socket to an address and port (done above).
    # 2. recvfrom() Receive data from the socket. It returns a tuple (data, address). No connection prior required.
    # 3. sendto() Send data to the socket. It requires the data and the address to send to.
    # 4. close() Close the socket when done.
    # 5. settimeout() Set a timeout for blocking socket operations.


    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
    
            response = b""
    
            udp_socket.sendto(response, source)



        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
