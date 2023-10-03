import os
import threading
import math

def startReceiver(n,index,fileName):
    os.system(f"python receiver.py {n} {index} {fileName}")

numberOfReceivers = int(input("Enter number of receivers:"))
receivers = []

if (math.log(numberOfReceivers)/math.log(2))%1==0:
	n = numberOfReceivers
else:
	n = 2**int((math.log(numberOfReceivers)/math.log(2))+1)

for i in range(numberOfReceivers):
    startReceiverThread = threading.Thread(target = startReceiver,args = (n,i,f"writtenFiles/file{i+1}.txt"))
    receivers.append(startReceiverThread)
    startReceiverThread.start()

for i in range(numberOfReceivers):
    receivers[i].join()

print("Receiving finished...")
print("Connection closed...")
