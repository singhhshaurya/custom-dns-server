import socket
from typing import List, Tuple
import traceback
import sys
import random


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    for i in sys.argv:
        print(i)


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
    
    # OTHER POINTS
    # 1. single byte is automatically converted to int. to convert series of bytes use int.frombytes()

    def int16_to_bytes(n: int) -> bytes: 
        high = (n >> 8) & 0xFF # retrieves the high 8 bits of the 16 bit integer we put. 0xFF = 255 = 11111111 in binary.
        low = n & 0xFF  # lower 8 bits.
        return bytes([high, low]) # bytes() function takes an iterable of data and returns a byte object.
                                  # the data MUST BE OF 1 byte size. So we use a list of 2 elements, each of which is 1 byte long.
                                  # thats why we divided 16 bits to 2 8 bit numbers.  

    def header_to_bytes(header:dict, **changed_fields) -> bytes:

        for i in changed_fields:
            header[i] = changed_fields[i]


        block = ((header['qr']<<15) | (header['opcode']<<11)  | (header['aa']<<10) | (header['tc']<<9) | (header['rd']<<8) | 
                     (header['ra']<<7) | (header['z']<<4) | header['rcode'])     
            
        header_section = (int16_to_bytes(header['id']) + int16_to_bytes(block) + int16_to_bytes(header['qdcount']) 
                              + int16_to_bytes(header['ancount']) + int16_to_bytes(header['nscount'])+ int16_to_bytes(header['arcount']))
        
        return header_section

    def generate_header(request_header) -> dict:
                
        id_ = int.from_bytes(request_header[0:2], byteorder="big", signed=False)

        # byte 2: QR OPCODE AA TC RD
        qr     = (request_header[2] & 0b10000000) >> 7
        opcode = (request_header[2] & 0b01111000) >> 3
        aa     = (request_header[2] & 0b00000100) >> 2
        tc     = (request_header[2] & 0b00000010) >> 1
        rd     =  request_header[2] & 0b00000001

        # byte 3: RA Z RCODE
        ra     = (request_header[3] & 0b10000000) >> 7
        z      = (request_header[3] & 0b01110000) >> 4
        rcode  =  request_header[3] & 0b00001111

        qdcount = int.from_bytes(request_header[4:6],  byteorder="big", signed=False)
        ancount = int.from_bytes(request_header[6:8],  byteorder="big", signed=False)
        nscount = int.from_bytes(request_header[8:10], byteorder="big", signed=False)
        arcount = int.from_bytes(request_header[10:12], byteorder="big", signed=False)

        # 6 16-bits block banenge, 12 bytes.
        # 1 block khud se banana padega pura of all the remaining ones.
        return{"id":id_, "qr":qr, "opcode":opcode, "aa":aa, "tc":tc, "rd":rd, "ra":ra, "z":z, "rcode":rcode, "qdcount":qdcount, "ancount":ancount, "nscount":nscount, "arcount":arcount}



    def questions_generator(query_question_section) -> List:
        records = [] # contains [labels+qtype+qclass]

        def fetch_record(ptr):
            record = b""
            while query_question_section[ptr] != 0:
                if query_question_section[ptr]>>6 == 3: # first bits are 11, compression. its a pointer.
                    ptr2 = ((query_question_section[ptr] & 0x3f) << 8) | query_question_section[ptr+1] - 12 # 2 bytes is the pointer excluding first 2 bits.
                    record += fetch_record(ptr2)[0][:-4] # only take the domain name. 
                    ptr += 2
                    break

                else:
                    length = query_question_section[ptr]
                    record += query_question_section[ptr:ptr+length+1]
                    ptr += length + 1

            record += query_question_section[ptr:ptr+5] # adding qtype and qclass, both 2 bytes.
            return record, ptr + 5
        
        ptr = 0
        while ptr < len(query_question_section):
            record, ptr = fetch_record(ptr)
            records.append(record)

        return records

                    

    def resolve_question(question, start_pos):
        upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # not binded, free socket for sending data.
        upstream_socket.settimeout(3)

        # UPSTREAM = ("1.1.1.1", 53) # address of an upstream resolver, this is cloudflare.
        ip, port = sys.argv[-1].split(":")
        UPSTREAM = (ip, int(port))

        upstream_id = random.randint(0, 65535)
        upstream_header = header_to_bytes(header.copy(), id = upstream_id, qdcount=1, ancount=0, nscount=0, arcount=0)

        try:
            upstream_socket.sendto(upstream_header+question, UPSTREAM)
            resolved_answer, _ = upstream_socket.recvfrom(512)

            response_id = int.from_bytes(resolved_answer[0:2], "big")
            if response_id != upstream_id:
                raise ValueError("Mismatched upstream DNS response ID")

            rcode = resolved_answer[3] & 0x0F
            if rcode != 0:
                return b"", 0, 0, 0, rcode # ANY OTHER RCODE.

            ancount = int.from_bytes(resolved_answer[6:8],  byteorder="big")
            nscount = int.from_bytes(resolved_answer[8:10], "big")
            arcount = int.from_bytes(resolved_answer[10:12], "big")

            answer = resolved_answer[12+len(question):] # remove question and header.its answer+auth+(other section).

            # now we fix the pointers send by the resolver to our actual answer.

            ptr = 0
            # print("WALLAHI")
            while answer[ptr] != 0: 
                if answer[ptr] >> 6 == 3: # means pointer hai bsdwala.
                    points_to = ((answer[ptr] & 0x3f) << 8) | answer[ptr+1] 
                    points_to = points_to - (12+len(question)) + start_pos
                    answer = answer[:ptr] + int16_to_bytes(0xC000 | points_to) + answer[ptr+2:]
                    ptr += 2
                else:
                    ptr += answer[ptr] + 1

            return answer, ancount, nscount, arcount, rcode

        except Exception as e:
            print("upstream error:", e)
            return b"", 0, 0, 0, 2 # SERVFAIL. 
        finally:
            upstream_socket.close()




    def generate_answers(records, start_pos):
        final_answer = b''
        
        for question in records:
            answer, ancount, nscount, arcount, rcode = resolve_question(question, start_pos) # question processed by name servers. 

            if rcode != 0:
                header['rcode'] = rcode
                continue

            header['ancount'] += ancount
            header['nscount'] += nscount
            header['arcount'] += arcount


            final_answer += answer
            start_pos += len(answer)

        return final_answer
    

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Message received from {source}. \n")

            query_question_section = buf[12:]

            header = generate_header(buf[:12]) # 12 bytes
            questions = questions_generator(query_question_section)


            question_section = b"".join(questions) # uncompressed.

            answer_section = generate_answers(questions, 12 + len(question_section)) # resolve questions one by one
    
            header['qr'] = 1
            header['ra'] = 1
                
            header_section = header_to_bytes(header)


            response = header_section + question_section + answer_section
            print(f"Header:{header}\nquestions = {question_section}\nanswers = {answer_section}")
            print("\n")
            print(f"Query: {buf}\n Response: {response}")
            print("\n")

            udp_socket.sendto(response, source)



        except Exception as e:
            print(f"Error receiving data: {e}")
            # traceback.print_exc()
            break


if __name__ == "__main__":
    main()
