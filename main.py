from socket import *
from threading import Thread
import tkinter as tk


def send_message():
    message = entry.get()
    client_socket.sendall(message.encode())


def receive_message():
    while True:
        try:
            reply = client_socket.recv(1024)
            if not reply:
                break
            msg_label.config(text=f"from server: {reply.decode('utf-8')}")
        except ConnectionAbortedError:
            break


def close_connection():
    client_socket.sendall(b'exit')
    client_socket.close()
    root.destroy()


client_socket = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 8000

client_socket.connect((host, port))

root = tk.Tk()
root.title("Client")
root.geometry("400x300")
root.configure(background='light blue')

lbl=tk.Label(root,text="Please, enter your comment here")
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

msg_label = tk.Label(root, text="",bg='light blue',fg='black')
msg_label.pack(pady=10)

close_button = tk.Button(root, text="Close Connection", command=close_connection)
close_button.pack()

receive_thread = Thread(target=receive_message)
receive_thread.start()

root.mainloop()
