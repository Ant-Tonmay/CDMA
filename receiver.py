import socket
import threading
import time
import sys

SERVER = "127.0.1.1"
PORT = 12345
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
n = int(sys.argv[1])
index = int(sys.argv[2])


receiver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
receiver.connect(ADDR)

w = [[1]]
while len(w)<n:
	n2 = 2*len(w)
	w2 = [[0 for i in range(n2)] for j in range(n2)]
	for i in range(n2):
		for j in range(n2):
			if i>=len(w) and j>=len(w):
				w2[i][j] = -w[i%len(w)][j%len(w)]
			else:
				w2[i][j] = w[i%len(w)][j%len(w)]
	w = w2
print(w)
try:
	with open(sys.argv[3],"w") as file:
		msg = ""
		while True:
			recvData = receiver.recv(1024).decode()
			# print(f'recvd data : {recvData}')
			data = [int(i) for i in recvData.split()]
			# print(f'data : {data}')
			bit = 0
			for i in range(n):
				bit += data[i]*w[index][i]
				# print(f'bit : {bit}')
			bit = bit//n
			if bit == -1:
				bit = "0"
			else:
				bit = "1"
			msg = msg+bit
			# print(f'mssg : {msg}')
			if len(msg)==8:
				ch = int(msg,2)
				if ch!=0:
					file.write(chr(ch))
				msg = ""
	receiver.close()
except:
	receiver.close()
