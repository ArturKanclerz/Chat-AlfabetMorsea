#!/usr/bin/env python3
import os
from Tkinter import Radiobutton, Button, Label
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from pygame import mixer
import tkinter
import time

sound_dict = {
    'a': "Sounds/A_morse_code.mp3"
}

image_dict = {
    'a': ("yellow", "red", "grey")

}



def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
            msg_list.see(tkinter.END)
        except OSError:
            break


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.geometry("1000x550")
top.title("Chat - Kanclerz & Romaniuk")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
# this will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
var = tkinter.IntVar()
tapy = 170
var.set(0)
Radiobutton(text='Tekst', value=0, variable=var).place(x=840, y=180)
Radiobutton(text='Dekodowanie', value=1, variable=var).place(x=840, y=205)
Radiobutton(text='Kodowanie', value=2, variable=var).place(x=840, y=230)
Radiobutton(text='Sygnaly dzwiekowe', value=3, variable=var).place(x=840, y=255)
Radiobutton(text='Sygnaly graficzne', value=4, variable=var).place(x=840, y=280)

imageLabel = Label(top, text="Wiadomosc graficzna", fg="black", font="Helvetica")
imageLabel.place(x=-10, y=230, height=30, width=200)

image = Button(font="Helvetica", bg="grey")
image.place(x=40, y=290, height=100, width=100)

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# Socket part
HOST = '127.0.0.1'  # Enter host of the server without inverted commas
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # for start of GUI  Interface
