# Chatbot
Simple chatbot using tcp connections and Markov chains.

# Usage
This script requires python3[https://www.python.org/].

To use ChatBot, simple clone or download this repository onto your computer and navigate into the folder within your shell.
Since we are using the TCP/IP protocol, we'll need to open this folder on another separate window as well.

In one window, run
```bash
python3 server.py <port>
```
where you may indicate a port number (4-digit port numbers work best).

In the second window, run
```bash
python3 client.py localhost <port>
```
where the two port numbers must match.
