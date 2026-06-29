# DNS (Domain Name System) Server
- DNS is a hierarchical and decentralized naming system for computers, services, or other resources connected to the Internet or a private network. It translates human-readable domain names (like www.example.com) into IP addresses like 192.168.1.1.

- DNS Servers are responsible for resolving domain names to IP addresses. When a user types a domain name into their browser, the request is sent to a DNS server, which looks up the corresponding IP address and returns it to the user's device.


## HOW DNS WORKS
1. **User Request**: A user enters a domain name in their web browser.
2. **DNS Query**: The browser sends a DNS query to the local DNS resolver (usually provided by the user's ISP).
3. **Recursive Resolution**: If the local resolver doesn't have the answer, it queries other DNS servers in a recursive manner until it finds the authoritative server for the domain.
4. **Authoritative Response**: The authoritative DNS server responds with the IP address associated with
5. **Response to User**: The local resolver sends the IP address back to the user's device, allowing the browser to connect to the web server hosting the requested domain.

## DNS PROTOCOL
- DNS uses the User Datagram Protocol (UDP) for most queries, but it can also use Transmission Control Protocol (TCP) for larger responses or zone transfers.
  
- UDP used because it is faster and requires less overhead than TCP. However, if the response data size exceeds 512 bytes, TCP is used to ensure reliable delivery.
  
- If data is less than 512 bytes, UDP is preferred for its speed and efficiency.
   
- DNS uses UDP because DNS queries are usually small, independent, and latency-sensitive. No 3 way connection, it just requires a response for a request quickly. 
  
- UDP dont guarantee reliable delivery, but DNS is designed to handle this by allowing clients to retry queries if no response is received. DNS client handles retries and timeouts, making it suitable for the quick nature of DNS lookups.






## DNS COMMUNICATION FORMAT
- All communications in the DNS protocol (both dns question and dns reply)are carried in a single format called a "message". Each message consists of 5 sections: header, question, answer, authority, and an additional space.
  
- 1. Header: Contains metadata about the message, such as the type of query, response code, and flags.
- 2. Question: Contains the domain name being queried and the type of record requested (e.g., A, AAAA, MX).
- 3. Answer: Contains the resource records that answer the query, including the IP address
- 4. Authority: Contains information about the authoritative name servers for the queried domain.
- 5. Additional: Contains additional information that may be useful for the client, such as IP addresses of other name servers.
  

### DNS QUERY PACKET
- A DNS query packet is sent from a client to a DNS server to request information about a specific domain name. 
- It contains no answer section, authority section, or additional section. The query packet consists of the header and question sections only.
- In the header, ANCOUNT, NSCOUNT, and ARCOUNT are set to 0, indicating that there are no answers, authority records, or additional records in the query packet.

### DNS RESPONSE PACKET
- A DNS response packet is sent from a DNS server to a client in response to a query. It contains the header, question, answer, authority, and additional sections.
- In the header, QDCOUNT is set to the number of questions in the query, while ANCOUNT, NSCOUNT, and ARCOUNT are set to the number of answers, authority records, and additional records included in the response packet.

### ADDITIONAL INFORMATION
  1. RECORD: a single entry in the DNS database that maps a domain name to an IP address or other information.
  2. RESOURCE RECORD (RR): a data structure that contains information about a domain name, including its IP address, type of record, and other metadata. Each RR consists of several fields, including NAME, TYPE, CLASS, TTL, RDLENGTH, and RDATA.
  3. TYPE: a 16-bit field that specifies the type of record being requested or returned. Common types include A (IPv4 address), AAAA (IPv6 address), MX (mail exchange), and CNAME (canonical name).
  4. CLASS: a 16-bit field that specifies the class of the record being requested or returned. The most common class is IN (Internet), which has a value of 1.Other classes include CH (Chaos) and HS (Hesiod).
  5. RDATA: the actual data associated with a resource record, which varies depending on the type of record. For example, for an A record, RDATA contains the IPv4 address, while for an MX record, it contains the mail server's hostname.







## HEADER SECTION STRUCTURE
| Field                              | Size    | Description                                                                 |
|------------------------------------|---------|-----------------------------------------------------------------------------|
| Packet Identifier (ID)             | 16 bits | A random ID assigned to query packets. Response packets must reply with the same ID. |
| Query/Response Indicator (QR)      | 1 bit   | 1 for a reply packet, 0 for a question packet.                              |
| Operation Code (OPCODE)            | 4 bits  | Specifies the kind of query in a message.                                   |
| Authoritative Answer (AA)          | 1 bit   | 1 if the responding server "owns" the domain queried, i.e., it's authoritative. |
| Truncation (TC)                    | 1 bit   | 1 if the message is larger than 512 bytes.                                  |
| Recursion Desired (RD)             | 1 bit   | Sender sets this to 1 if the server should recursively resolve this query, 0 otherwise. |
| Recursion Available (RA)           | 1 bit   | Server sets this to 1 to indicate that recursion is available.              |
| Reserved (Z)                       | 3 bits  | Used by DNSSEC queries. At inception, it was reserved for future use.        |
| Response Code (RCODE)              | 4 bits  | Response code indicating the status of the response.                        |
| Question Count (QDCOUNT)           | 16 bits | Number of questions in the Question section.                                |
| Answer Record Count (ANCOUNT)      | 16 bits | Number of records in the Answer section.                                    |
| Authority Record Count (NSCOUNT)   | 16 bits | Number of records in the Authority section.                                 |
| Additional Record Count (ARCOUNT)  | 16 bits | Number of records in the Additional section.                                |
                                     TOTAL: 96 bits(12 bytes)



- The header section is always 12 bytes (96 bits) long, regardless of the number of questions or answers in the message.
- Integers are encoded in *big endian* (network byte order) format, meaning the most significant byte is stored first.

https://github.com/EmilHernvall/dnsguide/blob/b52da3b32b27c81e5c6729ac14fe01fef8b1b593/chapter1.md contains a detailed explanation of the DNS protocol.




## QUESTION SECTION STRUCTURE
- The question section contains the domain name being queried and the type of record requested. It consists of the following fields:

QNAME    variable length
QTYPE    2 bytes
QCLASS   2 bytes

1. **QNAME**: The domain name being queried, represented as a sequence of labels. Each label is prefixed with a one byte length, and the entire domain name is terminated with a zero-length label (0x00). Its VARIABLE LENGTH.

Each label can be only upto 63 bytes long, and the total length of the domain name (including label lengths and the terminating zero) cannot 
exceed 255 bytes as only 1 byte is used to represent total length.
Label is 63 bytes because top 2 bits of length byte are reserved for special encodings, especially compression pointers.

   
2. **QTYPE**: A 16-bit field specifying the type of record being requested (e.g., A, AAAA, MX). 16 bits/2bytes

3. **QCLASS**: A 16-bit field specifying the class of the query. The most common class is IN (Internet), which has a value of 1. 16 bits/2bytes

- One complete record of qname, qtype, and qclass is called a "question". The number of questions in the message is specified by the QDCOUNT field in the header section.
  
-EXAMPLE: for the domain name "www.google.com", the QNAME would be represented as follows:
*\x03www\x06google\x03com\x00* + *\x00\x01\x00\x01* : \x03 indicates the length of the first label "www", \x06 indicates the length of the second label "google", \x03 indicates the length of the third label "com", and \x00 indicates the end of the domain name.

IN HEX: 03 77 77 77 06 67 6F 6F 67 6C 65 03 63 6F 6D 00

- Each '.' divides the url to labels, and each label is prefixed with its length. The total length of the QNAME field is variable, depending on the length of the domain name being queried.


## ANSWER SECTION STRUCTURE
- The answer section contains a list of RRs (Resource Records), which are answers to the questions asked in the question section.
- Each RR consists of the following fields:

NAME      variable length
TYPE      2 bytes
CLASS     2 bytes
TTL       4 bytes
RDLENGTH  2 bytes
RDATA     variable length


- 1. *NAME*: The domain name to which this resource record pertains. It is represented in the same format as QNAME in the question section. VARIABLE LENGTH. example: *\x03www\x06google\x03com\x00*. copy paste from question section.
  
- 2. *TYPE*: A 16-bit field specifying the type of record (e.g., A, AAAA, MX). 16 bits/2bytes
  
- 3. *CLASS*: A 16-bit field specifying the class of the record. The most common class is IN (Internet), which has a value of 1. 16 bits/2bytes
- 4. *TTL*: A 32-bit field specifying the time-to-live (in seconds) for this record. It indicates how long the record can be cached by a resolver before it should be discarded. 32 bits/4bytes
- 5. *RDLENGTH*: A 16-bit field specifying the length of the RDATA field in bytes. 16 bits/2bytes
- 6. *RDATA*: The actual data of the resource record, which varies depending on the TYPE of the record. For example, for an A record, RDATA contains the IPv4 address (4 bytes), while for an AAAA record, it contains the IPv6 address (16 bytes). VARIABLE LENGTH





