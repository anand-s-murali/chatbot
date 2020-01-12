/* client usage: ./client <hostname> <port> */

/**
 * Client:
 *		Socket
 *		Connect
 *		Send/Receive
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netdb.h>
#include <strings.h>
#include <arpa/inet.h>
#include <sys/types.h>

#define MAXLINE 1024 // the maximum number of characters we can receive

/**
 * Display error message and terminate process.
 * @param {char} *message The message to be printed.
 */
void error(char *message) {
	perror(message);
	exit(1);
}

int create_socket(char *host, int port) {
	int socketfd; // the socket file descriptor
	struct sockaddr_in server_addr;
	struct hostent *server; // the hostent structure is used to store information about the host (server) such as hostname, IP4, etc.
	
	// create the socket; error check
	if((socketfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		error("socket");
	}

	// receive information about the server
	if((server = gethostbyname(host)) == NULL) {
		error("invalid host - gethostbyname");
	}

	// socket requires we zero out the sockaddr_in structure
	bzero((char *) & server_addr, sizeof(server_addr));

	// update server info.
	server_addr.sin_family = AF_INET;
	// need to use bcopy to copy info from hostent to sockaddr_in
	// specifically, we need the address!
	bcopy((char *) server->h_addr, (char *) &server_addr.sin_addr.s_addr, server->h_length);
	server_addr.sin_port = htons(port); // need to use network-byte order for port
	
	// connect; error check
	if((connect(socketfd, (struct sockaddr *) &server_addr, sizeof(server_addr))) < 0) {
		error("connect");
	}	

	// return the socket descriptor for use
	return  socketfd;
}

/**
 * All code originates/starts from main.
 * @param {int} argc Number of command line arrguments.
 * @param {char} *argv[] Null-terminated list command arguments
 * @return {int} The return status of this process
 */
int main(int argc, char *argv[]) {
	int port; // the port the server is associated with
	char *host; // the host we are connecting to
	int socketfd; // the socket file descriptor used for communicating
	int bytes_sent, bytes_recv; // the number of bytes sent and received to/from the server
	char buffer[MAXLINE]; // used to store messages received from the server

	// check for usage
	if(argc < 3) {
		printf("usage: %s <hostname> <port>\n", argv[0]);
		exit(1);
	}

	// get hostname and port
	host = argv[1];
	port = atoi(argv[2]);

	// use host and port to get socket descriptor
	socketfd = create_socket(host, port);
	
	// receive message from server; error check
	if((bytes_recv = recv(socketfd, buffer, MAXLINE, 0)) < 0) {
		error("receive");
	}

	// display message received
	printf("Message containing %d bytes received from server.\nMessage: %s", bytes_recv, buffer);

	// close connection
	close(socketfd);

	// terminate process
	return 0;
}
