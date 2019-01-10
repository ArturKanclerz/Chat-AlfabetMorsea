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
    'b': "Sounds/B_morse_code.mp3",
    'c': "Sounds/C_morse_code.mp3",
    'd': "Sounds/D_morse_code.mp3",
    'e': "Sounds/E_morse_code.mp3",
    'f': "Sounds/F_morse_code.mp3",
    'g': "Sounds/G_morse_code.mp3",
    'h': "Sounds/H_morse_code.mp3",
    'i': "Sounds/I_morse_code.mp3",
    'j': "Sounds/J_morse_code.mp3",
    'k': "Sounds/K_morse_code.mp3",
    'l': "Sounds/L_morse_code.mp3",
    'm': "Sounds/M_morse_code.mp3",
    'n': "Sounds/N_morse_code.mp3",
    'o': "Sounds/O_morse_code.mp3",
    'p': "Sounds/P_morse_code.mp3",
    'q': "Sounds/P_morse_code.mp3",
    'r': "Sounds/R_morse_code.mp3",
    's': "Sounds/S_morse_code.mp3",
    't': "Sounds/T_morse_code.mp3",
    'u': "Sounds/U_morse_code.mp3",
    'v': "Sounds/V_morse_code.mp3",
    'w': "Sounds/W_morse_code.mp3",
    'x': "Sounds/X_morse_code.mp3",
    'y': "Sounds/Y_morse_code.mp3",
    'z': "Sounds/Z_morse_code.mp3"

}

image_dict = {
    'a': ("yellow", "red", "grey"),
    'b': ("red", "yellow", "yellow", "yellow", "grey"),
    'c': ("red", "yellow", "red", "yellow", "grey"),
    'd': ("red", "yellow", "yellow", "grey"),
    'e': ("yellow", "grey"),
    'f': ("yellow", "yellow", "red", "yellow", "grey"),
    'g': ("red", "red", "yellow", "grey"),
    'h': ("yellow", "yellow", "yellow", "yellow", "grey"),
    'i': ("yellow", "yellow", "grey"),
    'j': ("yellow", "red", "red", "red", "grey"),
    'k': ("red", "yellow", "red", "grey"),
    'l': ("yellow", "red", "yellow", "yellow", "grey"),
    'm': ("red", "red", "grey"),
    'n': ("red", "yellow",  "grey"),
    'o': ("red", "red", "red", "grey"),
    'p': ("yellow", "red", "red", "yellow", "grey"),
    'q': ("red", "red", "yellow", "red", "grey"),
    'r': ("yellow", "red", "yellow", "grey"),
    's': ("yellow", "yellow", "yellow", "grey"),
    't': ("red", "grey"),
    'u': ("yellow", "yellow", "red", "grey"),
    'v': ("yellow", "yellow", "yellow", "red", "grey"),
    'w': ("yellow", "red", "red", "grey"),
    'x': ("red", "yellow", "yellow", "red", "grey"),
    'y': ("red", "yellow", "red", "red","grey")


}


def receive():
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


def change_to_sound(msg = ""):
    prefix = msg[1:msg.index(':')+1]
    just_msg = msg[msg.index(':') + 1:]
    prefix = prefix[0].upper() + prefix[1:]
    msg_list.insert(tkinter.END, prefix + " Playing song...")
    msg_list.see(tkinter.END)
    for i in range(len(just_msg)):
        if sound_dict.get(just_msg[i]) is not None:
            mixer.init()
            mixer.music.load(os.path.abspath(sound_dict.get(just_msg[i])))
            mixer.music.play()
            time.sleep(2)


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
    prefix = prefix[0].upper() + prefix[1:]
    print prefix
    msg_list.insert(tkinter.END, prefix + " Rendering graphical message...")
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

def send(check, event=None):

    global c
    if check is False:
        msg = my_msg.get()
        nick ="Your nick: " + msg
        nickLabel = Label(top, text=nick, bg="#33CC00", fg="black", font="Helvetica")
        nickLabel.place(x=-10, y=100, height=30, width=220)
        c = True
    else:
        msg = var.get().__str__() + my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg))
    if msg[1:] == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    sendd()


top = tkinter.Tk()
top.geometry("1250x620")
top.title("Chat - Kanclerz & Romaniuk")
top.configure(bg="#716664")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=29, width=86, bg="#99FFFF", yscrollcommand=scrollbar.set, font =10)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
var = tkinter.IntVar()
tapy = 170
var.set(0)
Radiobutton(text='Text', value=0, variable=var).place(x=1100, y=180)
Radiobutton(text='Decoding', value=1, variable=var).place(x=1100, y=205)
Radiobutton(text='Encoding', value=2, variable=var).place(x=1100, y=230)
Radiobutton(text='Sound signals', value=3, variable=var).place(x=1100, y=255)
Radiobutton(text='Graphic signals', value=4, variable=var).place(x=1100, y=280)

imageLabel = Label(top, text="Graphic Message", bg="#33CC00", fg="black", font="Helvetica")
imageLabel.place(x=-10, y=280, height=30, width=200)
optionsLabel = Label(top, text="Choose option", bg="#33CC00", fg="black", font="Helvetica")
optionsLabel.place(x=1050, y=130, height=30, width=200)

image = Button(font="Helvetica", bg="grey")
image.place(x=40, y=340, height=100, width=100)

entry_field = tkinter.Entry(top, width="132",  textvariable=my_msg)
entry_field.bind("<Return>", sendd)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=sendd)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


HOST = '127.0.0.1'
PORT = 33006
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
