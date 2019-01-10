import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from pygame import mixer, time


encode_dict = {
    'a': ".-",
    'b': "-...",
    'c': "-.-.",
    'd': "-..",
    'e': ".",
    'f': "..-.",
    'g': "--.",
    'h': "....",
    'i': "..",
    'j': ".---",
    'k': "-.-",
    'l': ".-..",
    'm': "--",
    'n': "-.",
    'o': "---",
    'p': ".--.",
    'q': "--.-",
    'r': ".-.",
    's': "...",
    't': "-",
    'u': "..-",
    'v': "...-",
    'w': ".--",
    'x': "-..-",
    'y': "-.--",
    'z': "--..",
    ' ': ' '
}

decode_dict = {
    ".-": 'a',
    "-...": 'b',
    "-.-.": 'c',
    "-..": 'd',
    ".": 'e',
    "..-.": 'f',
    "--.": 'g',
    "....": 'h',
    "..": 'i',
    ".---": 'j',
    "-.-": 'k',
    ".-..": 'l',
    "--": 'm',
    "-.": 'n',
    "---": 'o',
    ".--.": 'p',
    "--.-": 'q',
    ".-.": 'r',
    "...": 's',
    "-": 't',
    "..-": 'u',
    "...-": 'v',
    ".--": 'w',
    "-..-": 'x',
    "-.--": 'y',
    "--..": 'z'
}


def decode(msg):
    pom = " "
    list_of_char = msg.split(' ')
    print "TEST"
    print list_of_char
    print list_of_char
    for char in list_of_char:
        if decode_dict.get(char) is not None:
            pom += decode_dict.get(char)
        else:
            pom += " "
    print "pom=" + pom
    return pom


def encode(msg):
    pom = " "

    for i in range(len(msg)):
        if encode_dict.get(msg[i]) is not None:
            pom += encode_dict.get(msg[i])
            pom += " "

    return pom



def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes(" Witaj w chacie! Wpisz swoj nick i nacisnij Enter"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()



def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = ' Witaj %s! Jezeli chcesz zakonczyc wpisz {quit}.' % name
    client.send(bytes(welcome))
    msg = " %s has joined the chat!" % name
    broadcast(bytes(msg))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg[1:] != bytes("{quit}"):
            if msg[0] == '0':
                broadcast(msg, name+": ")
            if msg[0] == '1':
                broadcast(decode(msg[1:].lower()), name + ": ")
            if msg[0] == '2':
                broadcast(encode(msg.lower()), name + ": ")
            if msg[0] == '3':
                broadcast(msg, name + ": ")
            if msg[0] == '4':
                broadcast(msg, name + ": ")

        else:
            client.send(bytes("{quit}"))
            client.close()
            del clients[client]
            broadcast(bytes(" %s has left the chat." % name))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(msg[0] + bytes(prefix) + msg[1:])


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33006
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print(" Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
