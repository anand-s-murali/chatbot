/* server usage: ./server <port> */

/**
 * Server: 
 *		Socket
 *		Bind
 *		Listen
 *		Accept
 *		Send/recv
 */		

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <strings.h>
#include <unistd.h>
#include <sys/types.h>
#include <arpa/inet.h>

/**
 * Display error message and terminate process.
 * @param {char} *message The message to be printed.
 */
void error(char *message) {
	perror(message);
	exit(1);
}

/**
 * Creates the socket to be used by the server.
 * @param {int} port The port associated with this server process.
 * @return {int} The status of the socket descriptor.
 */
int create_socket(int port) {
	int socketfd; // the socket descriptor
	struct sockaddr_in server; // need a sockaddr_in structure for the server to set/store the information

	// create the socket; error check
	// we are using TCP connection
	if((socketfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		error("socket");
	}

	// set the server information for sockaddr_in
	server.sin_family = AF_INET; // IPv4 usage
	server.sin_port = htons(port); // need to use network-byte order for port
	server.sin_addr.s_addr = INADDR_ANY;

	// the socket API also requires us to zero out the bytes of the sockaddr_in structure
	bzero(&server.sin_zero, sizeof(server.sin_zero));

	// bind the server; error check
	if((bind(socketfd, (struct sockaddr *) &server, sizeof(server))) < 0) {
		error("bind");
	}

	// listen for connection
	if((listen(socketfd, 5)) < 0) {
		error("listen");
	}

	// return our socket descriptor for use!
	return socketfd;
}

/**
 * All code originates/starts from main.
 * @param {int} argc Number of command line arrguments.
 * @param {char} *argv[] Null-terminated list command arguments
 * @return {int} The return status of this process
 */ 
int main(int argc, char *argv[]) {
	int port; // the port to be used by this server
	int serverfd; // the server socket file descriptor (will be taken from create_socket)
	int clientfd; // the socket descriptor for the client
	int bytes_sent, bytes_recv; // the number of bytes sent and received from/to client
	char message[] = "Hello from chatbot server!\n";
	struct sockaddr_in client_conn; // the client connection used for accept()
	
	// check usage
	if(argc < 2) {
		printf("usage; %s <port>\n", argv[0]);
		exit(1);
	}

	// set the port
	port = atoi(argv[1]);

	// get socket descriptor for server
	serverfd = create_socket(port);
	if(serverfd < 0) {
		error("socket error");
	}

	printf("Server awaiting connections...\n");
	
	// now that we have the server's socket descriptor, we may "run" the server
	socklen_t client_len = sizeof(client_conn);
	while(1) {
		// accept connection if present
		if((clientfd = accept(serverfd, (struct sockaddr *) &client_conn, &client_len)) < 0) {
			error("accept");
		}

		// send message to client
		if((bytes_sent = send(clientfd, message, strlen(message), 0)) < 0) {
			error("send");
		}

		// print some server-side confirmation information
		printf("Message containing %d bytes sent to client located at %s\n", bytes_sent, inet_ntoa(client_conn.sin_addr));

		// close connection with client
		close(clientfd);	
	}

	return 0;
}
