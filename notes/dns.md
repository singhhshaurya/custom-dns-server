# DNS - DOMAIN NAME SYSTEM
- Definition: The Domain Name System (DNS) is a hierarchical and decentralized naming system for computers, services, or other resources connected to the Internet or a private network. It translates human-readable domain names (like www.example.com) into IP addresses (like 93.184.216.34).


# ELEMENTS OF DNS
1. **Domain Names**: Human-readable addresses that are easier to remember than numerical IP addresses.
2. **IP Addresses**: Numerical labels assigned to devices on a network, used for identifying
3. **Domain Name Space**: The hierarchical structure of domain names, organized in levels (e.g., top-level domains, second-level domains).
4. **Resource Records (RRs)**: Entries in the DNS database that provide information about a domain, such as its IP address, mail server, or other services.
5. **Name servers**: Servers that store DNS records and respond to queries from clients, helping to resolve domain names to IP addresses.
6. **Resolvers**: Client-side components that send DNS queries to name servers and receive responses, facilitating the translation of domain names to IP addresses.

7. **Authoritative Name Servers**: These servers hold the definitive records for a domain and can provide answers to queries about that domain.
8. **Caching**: The process of storing DNS query results temporarily to reduce the load on authoritative name servers and speed up subsequent queries for the same domain.

Client enters a domain name in the browser -> Resolver sends a query to the DNS server -> DNS server looks up the domain name in its database -> If found, it returns the corresponding IP address to the resolver -> Resolver sends the IP address back to the client -> Client uses the IP address to establish a connection with the desired server.

