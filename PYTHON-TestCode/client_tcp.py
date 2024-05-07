import socket
from threading import Thread
import time

addrPort_sending = ("192.168.137.76", 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(addrPort_sending)
running = [True]

list_messages = []

def receive_msg():
    try:
        print("listening to message")
        msg_server = s.recv(1024)
        list_messages.append(msg_server)
    except Exception as e :
        print(e)

def send_message():
    time.sleep(0.1)
    msgClient = input("message : ")
    msgToSend = str.encode(msgClient)
    s.send(msgToSend)

    if msgClient == "KILL" or msgClient == "STOP":
        s.close()
        running[0] = False


task_receive = Thread(target=receive_msg, daemon=False)
task_receive.start()
task_sending = Thread(target=send_message, daemon=False)
task_sending.start()
while running[0]:

    if not task_sending.is_alive():
        task_sending = Thread(target=send_message)
        task_sending.start()    
    

task_receive.join(0)
task_sending.join(0)
