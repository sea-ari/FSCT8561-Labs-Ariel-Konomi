

`socket.recv(buflen)`: This method receives data from the socket. The method argument indicates the maximum amount of data it can receive.
`socket.recvfrom(buflen)`: This method receives data and the sender's address.
`socket.recv_into(buffer)`: This method receives data into a buffer.
`socket.recvfrom_into(buffer)`: This method receives data into a buffer.
`socket.send(bytes)`: This method sends bytes of data to the specified target.
`socket.sendto(data, address)`: This method sends data to a given address.
`socket.sendall(data)`: This method sends all the data in the buffer to the socket.
`socket.close()`: This method releases the memory and finishes the connection.

`socket.bind(address)`: This method allows us to connect the address with the socket, with the requirement that the socket must be open before establishing the connection with the address.
`socket.listen(count)`: This method accepts as a parameter the maximum number of connections from clients and starts the TCP listener for incoming connections.
`socket.accept()`: This method enables us to accept client connections and returns a tuple with two values that represent client_socket and client_address. You need to call the socket.bind() and socket.listen() methods before using this method.


`socket.connect(ip_address)`: This method connects the client to the server IP address.
`socket.connect_ext(ip_address)`: This method has the same functionality as the connect() method and also offers the possibility of returning an error in the event of not being able to connect with that address.



**reverse shell** is an action by which a user gains access to the shell of an external server

`gethostbyaddr(address)`: This allows us to obtain a domain name from the IP address.
`gethostbyname(hostname)`: This allows us to obtain an IP address from a domain name.

`bind(IP,PORT)` method allows you to associate a host and a port with a specific socket, taking into account the fact that ports 1-1024 are reserved for the standard protocols


`server.listen(5)` instruction tells the server to start listening, with the maximum backlog of connections set to five clients