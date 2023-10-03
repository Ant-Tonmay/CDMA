import socket
import time
import sys

SERVER = "127.0.1.1"
PORT = 12345
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
TIMEDELAY = 0.1


sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sender.connect(ADDR)

try:
    with open(sys.argv[1]) as file:
        s = file.read()
        print(f'File content : {s}')
        maxLen = int(sys.argv[2])
        for ch in s:
            msg = str(bin(ord(ch))).replace("0b","")
            msg = (8-len(msg))*"0"+msg
            # print(f'Message : {msg}')
            for bit in msg:
                time.sleep(TIMEDELAY)
                # print(f'Sent bit : {bit}')
                sender.send(bit.encode(FORMAT))
        for i in range(len(s),maxLen):
            msg = 8*"0"
            for bit in msg:
                time.sleep(TIMEDELAY)
                # print(f'Sent bit : {bit}')
                sender.send(bit.encode(FORMAT))

        time.sleep(TIMEDELAY)
        sender.close()
except:
    sender.close()
