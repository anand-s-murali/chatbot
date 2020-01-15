'''
Continuation of chatbot using tcp/networking protocol.
'''

'''
    Client:
        socket
        connect
        send/recv
        close
'''

import socket
import errno
import sys

MAXLINE = 1024 # this will be the largest stream the server (and client) will be able to receive at a given time
encoding = 'utf-8' # encoding usage


'''
Get the number of bytes in a string.
@param {string} s The string to get bytes of.
'''
def get_bytes(s):
    return len(s.encode('utf-8'))

'''
All code 'starts' here.
'''
def main():
    bytes_sent = -1 # the total bytes sent to server
    bytes_recv = -1 # the total bytes received by server
    buff = '' # will store the message(s) going to/coming from the server

    # follows the instructions above!

    # check for usage
    if(len(sys.argv) < 3):
        print('usage: python3 {} <hostname> <port>\n'.format(sys.argv[0]))
        sys.exit(1)

    # get hostname and port information from system
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    try:
        # create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

        # connect to the server
        sock.connect((hostname, port))

        # receive first message
        buff = sock.recv(MAXLINE)
        bytes_recv = len(buff)
        buff = buff.decode(encoding)
        print(buff)

        print('You: ',end='')
        sys.stdout.flush()

        # now we may send/receive information from the server!
        for line in sys.stdin:
            # read input from user; remove newline!
            buff = line.rstrip()
            
            # check if we need to quit
            if(buff == 'exit'):
                break
            
            # send message to server
            bytes_sent = get_bytes(buff)
            sock.send(bytes(buff, encoding))

            # get message back
            buff = sock.recv(MAXLINE)
            bytes_recv = len(buff)
            buff = buff.decode(encoding)
            print('ChatBot: {}'.format(buff))

            # repeat!
            print('You: ',end='')
            sys.stdout.flush()


        # close the socket
        sock.close()
    except socket.error as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
