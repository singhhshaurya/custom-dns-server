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

    def int16_to_bytes(n: int) -> bytes: 
        high = (n >> 8) & 0xFF # retrieves the high 8 bits of the 16 bit integer we put. 0xFF = 255 = 11111111 in binary.
        low = n & 0xFF  # lower 8 bits.
        return bytes([high, low]) # bytes() function takes an iterable of data and returns a byte object.
                                  # the data MUST BE OF 1 byte size. So we use a list of 2 elements, each of which is 1 byte long.
                                  # thats why we divided 16 bits to 2 8 bit numbers.  

    def generate_header(request_message):
        # 
        id = 1234 # 16 bits.
        qr = 1 # 1 
        opcode = 0 # 4
        aa = 0 # 1
        tc = 0 # 1
        rd = 0 # 1
        ra = 0 # 1
        z = 0 # 3
        rcode = 0 # 4
        qdcount = 0 # 16
        ancount = 0 # 16
        nscount = 0 # 16
        arcount = 0 # 16

        # 6 16-bits block banenge, 12 bytes.
        # 1 block khud se banana padega pura of all the remaining ones.

        block = (qr<<15) + (opcode<<11)  + (aa<<10) + (tc<<9) + (rd<<8) + (ra<<7) + (z<<4) + rd
        return (int16_to_bytes(id) + int16_to_bytes(block) + int16_to_bytes(qdcount) + int16_to_bytes(ancount) + int16_to_bytes(nscount) 
                + int16_to_bytes(arcount))


    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
    

            header = generate_header(buf)

            response = header
    
            udp_socket.sendto(response, source)



        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
