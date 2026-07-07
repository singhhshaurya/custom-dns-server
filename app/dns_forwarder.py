
import socket
import sys



def main():
    for i in sys.argv:
        print(i)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # udp_socket.bind(("127.0.0.1", 2054)) 

    # while True:
    #     query, source = udp_socket.recvform()
    #     ip, port = sys.argv()["resolver"].split(":")

    #     udp_socket.sendto(query, (ip, int(port)))
    #     udp_socket.sendto()

    query = "12340100000100000000000006676f6f676c6503636f6d0000010001"
    query = b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01"


    udp_socket.sendto(query, ("1.1.1.1", 53))

    
    query, source = udp_socket.recvfrom(512)
    print("GOT THE ANSWER!")
    print(source, "\n", query.hex())







if __name__ == "__main__":
    main()