'''
A simple chatbot in python3 using tcp/networking protocols.
'''

'''
    Server:
        socket
        bind
        listen
        accept
        send/recv
        close
'''

from collections import defaultdict
import socket
import errno
import sys
import random

TEXT_FILE = 'text.txt'
MAXLINE = 1024 # this will be the largest stream the server (and ultimately the client) will be able to receive at a given time
encoding = 'utf-8'

'''
Get the number of bytes in a string.
@param {string} s The string to get bytes of.
'''
def get_bytes(s):
    return len(s.encode('utf-8'))

'''
Creates the markov sentence.
@param {dictionary} data The word mappings to be used.
@return {string} The final sentence.
'''
def generate_sentence(data):
    try:
        key = random.choice(list(data.keys()))
        sentence = []
        capital = True
        while len(sentence) < 20:
            value = random.choice(data[key])
            if value == '\n':
                break
            # add value to sentence
            if capital:
                sentence.append(value.capitalize())
                capital = False
            else:
                sentence.append(value.lower())

            # check if next word needs to be capitalized
            if value[-1] == '.' or value[-1] == '!' or value[-1] == '.':
                capital = True

            key = value
        # return the final sentence
        return ' '.join(sentence)+'.'
    except Exception as e:
        print(key, ' --> ', data[key])
        print(e)
        sys.exit(1)


'''
Handles all communication with the client (sends and receives messages).
@param {int} clientfd The client's socket desciptor
'''
def handle_client(clientfd, data):
    bytes_sent = 0 # store the number of bytes sent to client
    bytes_recv = 0 # store the number of bytes received by server
    buff = '' # store the messages we send/receive to/from client

    # send initial message
    buff = 'ChatBot: Welcome to ChatBot! Begin typing to get to know your bot! Enter the string \'exit\' when you are done.'
    clientfd.send(bytes(buff, encoding))

    # loop forever to continue
    while True:
        buff = clientfd.recv(MAXLINE)
        bytes_recv = len(buff)

        # check if we need to return
        if(bytes_recv == 0):
            return

        buff = buff.decode('utf-8').split()
        print('Received message ({}) consisting of {} bytes from client.'.format(buff, bytes_recv))
        
        #print('Attempting to reverse message ({}) for client...'.format(buff))
        # reverse the string
        #buff = buff[::-1]
        buff = generate_sentence(data)

        # send back to client
        bytes_sent = get_bytes(buff)
        clientfd.send(bytes(buff, encoding))

        print('Attempting to send message ({}) consisting of {} bytes back to client...'.format(buff, bytes_sent))

'''
'Trains' the ai by reading our text file and making a word mapping.
The map uses pairs of consecutive words as keys and the word succeeding the pair as the value.
@return {dictionary} The final word dictionary
'''
def train():
    try:
        data = defaultdict(list)
        words = []
        flag = '\n'
        last_word = flag
        with open(TEXT_FILE, 'r') as fp:
            line = fp.readline().split()
            while line:
                for i in range(len(line)-1):
                    # add to table
                    data[line[i]].append(line[i+1]) 
                last_word = line[len(line)-1]
                # need to end last word of every line with flag (just in case!)
                data[last_word].append(flag)
                line = fp.readline().split()
            

            # remove duplicates from lists
            for k,v in data.items():
                data[k] = list(set(data[k]))

            return data
    except Exception as e:
        print(e)
        sys.exit(1)
'''
All code 'starts' here.
Follows the procedure above.
'''
def main():
    # check for usage
    if(len(sys.argv) < 2):
        print('usage: python3 {} <port>\n'.format(sys.argv[0]))
        sys.exit(1)

    # update port
    port = int(sys.argv[1])

    # need to 'train' our ai
    data = train()
    
    try:
        # create the socket; using tcp connection
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

        # gets rid of Bind error: port already in use
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        # bind the socket to the port given by user
        server_sock.bind(('', port))

        # listen for impending/queued connections; we will accept 5 connections
        server_sock.listen(5)

        print('Server awaiting connections...\n')

        # loop forever
        while True:
            # get/accept connection from a client
            client_sock, client_addr = server_sock.accept()

            print('Client located at {} has connected to the server.'.format(client_addr))

            # handle client
            handle_client(client_sock, data)

            # close connection with client
            client_sock.close()
            
            print('Client located at {} has disconnected from the server.'.format(client_addr))

    except socket.error as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
