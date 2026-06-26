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
- All communications in the DNS protocol are carried in a single format called a "message". Each message consists of 5 sections: header, question, answer, authority, and an additional space.
- 1. Header: Contains metadata about the message, such as the type of query, response code, and flags.
- 2. Question: Contains the domain name being queried and the type of record requested (e.g., A, AAAA, MX).
- 3. Answer: Contains the resource records that answer the query, including the IP address
- 4. Authority: Contains information about the authoritative name servers for the queried domain.
- 5. Additional: Contains additional information that may be useful for the client, such as IP addresses of other name servers.

### HEADER SECTION STRUCTURE
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

