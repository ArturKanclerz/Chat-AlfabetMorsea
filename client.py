# !/usr/bin/env python3
import os
from Tkinter import Radiobutton, Button, Label
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from pygame import mixer
import tkinter
import time


sound_dict = {
    'a': "Sounds/A_morse_code.mp3",
    'b': "Sounds/B_morse_code.mp3"
}

image_dict = {
    'a': ("yellow", "red", "grey")

}




def receive():
    """Handles receiving of messages."""
    global c2
    while True:

        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg[0] == '3':
                change_to_sound(msg.lower())
            elif msg[0] == '4':
                change_to_image(msg.lower())
            else:
                msg_list.insert(tkinter.END, msg[1:])
                msg_list.see(tkinter.END)
            c2 = c2 + 1

        except OSError:
            break


c = False
c2 = 0


def change_to_sound(msg=""):
    return None


def return_delay_from_color(color=""):
    if color == "yellow":
        return 0.75
    if color == "grey":
        return 0.25
    if color == "red":
        return 2.25


def change_to_image(msg = ""):
    prefix = msg[1:msg.index(':') + 1]
    just_msg = msg[msg.index(':') + 1:]
    for i in range(len(just_msg)):
        if image_dict.get(just_msg[i]) is not None:

            temp_tuple = image_dict.get(just_msg[i])
            for el in temp_tuple:
                image.configure(bg=el)
                time.sleep(return_delay_from_color(el))
            image.configure(bg="grey")


def sendd(event=None):
    global c
    send(c)


def send(check, event=None):  # event is passed by binders.

    global c
    if check is False:
        msg = my_msg.get()
        c = True
        print "Jestem w check FALSE"
    else:
        msg = var.get().__str__() + my_msg.get()
        print "Jestem w check TRUE"
    print "Check: " + check.__str__()
    print "Wiadomosc do wyslania: " + msg
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    sendd()


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
entry_field.bind("<Return>", sendd)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=sendd)
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
