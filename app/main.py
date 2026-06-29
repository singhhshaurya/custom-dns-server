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
        qdcount = 1 # 16
        ancount = 0 # 16
        nscount = 0 # 16
        arcount = 0 # 16

        # 6 16-bits block banenge, 12 bytes.
        # 1 block khud se banana padega pura of all the remaining ones.

        block = (qr<<15) | (opcode<<11)  | (aa<<10) | (tc<<9) | (rd<<8) | (ra<<7) | (z<<4) | rcode
        return (int16_to_bytes(id) + int16_to_bytes(block) + int16_to_bytes(qdcount) + int16_to_bytes(ancount) + int16_to_bytes(nscount) 
                + int16_to_bytes(arcount))


    def parse_questions(message, qcount):
        print(message)

        questions = [] # contains [[labels], qtype, qclass]]
        records = [] # contains [labels+qtype+qclass]
        ptr = 0
        prev_record = 0

        for i in range(qcount):
            length = message[ptr]
            labels = []
            while length != 0:
                print(length)
                labels.append(message[ptr+1:ptr+length])
                ptr += length + 1
                length = message[ptr] 
            
            questions.append([labels, message[ptr+1:ptr+3], message[ptr+3:ptr+5]]) # last 4 bytes are for qtype and qclass
            ptr += 5 # NULL byte + 4 bytes skip (qtype and qclass)
            records.append(message[prev_record:ptr])
            prev_record = ptr

        return questions, records

    def parse_question(question):

        ttl = 60 # 4 bytes, 32 bits.
        rdlength = 4 # 2 bytes, 16 bits
        data = b"\x08\x08\x08\x08" # random ip address. this is 8.8.8.8

        ttl = int16_to_bytes(ttl>>16) + int16_to_bytes(ttl) # converting to 4 bytes.
        return ttl, int16_to_bytes(rdlength), data


    def generate_answers(records):
        answer = b''
        for question in records:
            ttl, rdlength, data = parse_question(question)
            answer += question + ttl + rdlength + data

        return answer





    
        return message # + int16_to_bytes(type) + int16_to_bytes(CLASS)

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Message received from {source}. \n{buf}\n")

            header = generate_header(buf[:12]) # 12 bytes
            question_section = buf[12:]
            
            questions, records = parse_questions(question_section, 1)
            answer_section = generate_answers(records)
            response = header + question_section + answer_section
            print(f"Header:{header}\nquestions = {question_section}\nanswers = {answer_section}")
            print(f"Response: {response}")
            print("\n")
    
            udp_socket.sendto(response, source)



        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
