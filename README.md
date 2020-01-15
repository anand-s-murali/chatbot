# Chatbot
Simple chatbot using tcp connections and Markov chains.

# Usage
This script requires [python3](https://www.python.org/)

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

# Behind the Scenes
Per Wikipedia's definition, a Markov Chain is " ...a stochastic model describing a sequence of possible events in which the probability of each event depends only on the state attained in the previous event." Indeed, this is precisely how the computer generates responses. To start the chain, a word, commonly known as the key, is randomly selected from the text, and from its list of successors, a random word, known as the value, is chosen. The key-value pair, now "linked," is added to a string, and our value is used as the next key, repeating the process until we reach the desired word length. This algorithm, while simple, is far from human. At best, the responses are incoherent, unintelligible, grammatically incorrect, and incredibly entertaining to read. 

# Changing the Source Text:
Courtesy of [Project Gutenberg](https://www.gutenberg.org/ebooks/), I used *Moby Dick or the Whale,* by Herman Melville as my source text, and is represented through text.txt. This can be changed, however. If you do intend on changing the source text and plan on using the entire text, it is advised to remove some forms of puncutation such as exclamation or question marks, quotes, commas, and blank lines (periods should be fine). This can easily be done in a text editor using find and replace, and is completely optional, however, it tends to make for better output.
