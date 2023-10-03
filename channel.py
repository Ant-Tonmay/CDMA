import socket
import threading
import time
import math

ip = "0.0.0.0"
PORT = 12345
ADDR = (ip,PORT)
FORMAT = "utf-8"
n = 1
senders = []
receivers = []
w = []
data = []
FINISHED = False
MSGLEN = 1024
numberOfSenders = 1
w = [[1]]

#take data from senders and encode them acc to walsh matrix
def recvData(index):
	global senders
	global data
	global n
	global numberOfSenders
	try:
		d = int(senders[index].recv(1).decode())
		if d==0:
			d = -1
		for i in range(n):
			data[i] += d*w[index][i]
	except:
		FINISHED = True
		for i in range(numberOfSenders):
			receivers[i].close()

def transmitData():
	global n
	global w
	global senders
	global receivers
	global data
	global FINISHED
	global numberOfSenders
	try:
		while not(FINISHED):
			data = [0 for i in range(n)]
			senderThreads = []
			for i in range(numberOfSenders):
				sThread = threading.Thread(target = recvData , args = (i,))
				senderThreads.append(sThread)
			for i in range(numberOfSenders):
				senderThreads[i].start()
			for i in range(numberOfSenders):
				senderThreads[i].join()

			data = [str(bit) for bit in data]
			msg = " ".join(data)
			print(f"Transmitting Data: {msg}")
			msg = (MSGLEN-len(msg))*' '+msg

			for i in range(numberOfSenders):
				receivers[i].send(msg.encode(FORMAT))
	except:
		FINISHED = True
		print("Transmition finished...")
		print("Connection closed...")
		for i in range(numberOfSenders):
			receivers[i].close()


channel = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
channel.bind(ADDR)

numberOfSenders = int(input("Enter number of senders:"))
#check number of senders!!
if numberOfSenders<=0:
	print("Invalid input!!!")
	exit()

#n is the diemnsion of Walsh matrix. It has to be power of 2, So the following codeblock...
if (math.log(numberOfSenders)/math.log(2))%1==0:
	n = numberOfSenders
else:
	n = 2**int((math.log(numberOfSenders)/math.log(2))+1)# rounds off to next power of 2


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

print("Walsh Code:")
print(w)

channel.listen(2*numberOfSenders)

print("\n\nWaiting for receivers...\n")
for i in range(numberOfSenders):
	conn , addr = channel.accept()
	print(f"Receiver {i+1} connected...")
	receivers.append(conn)
print("\n\n")

print("Waiting for senders...\n")
for i in range(numberOfSenders):
	conn , addr = channel.accept()
	print(f"Sender {i+1} connected...")
	senders.append(conn)
print("\n\n")

transmitDataThread = threading.Thread(target =  transmitData)
print("Transmission started...\n\n")
transmitDataThread.start()
transmitDataThread.join()

print("\n\nTransmitting finished...")
print("Connection closed...")
