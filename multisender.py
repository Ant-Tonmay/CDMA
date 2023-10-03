import os
import threading

def startSender(fileName,maxLen):
    os.system(f"python sender.py {fileName} {maxLen}")

numberOfSenders = int(input("Enter number of senders:"))
senders = []
maxLen = 0
for i in range(numberOfSenders):
    with open(f"dataFiles/file{i+1}.txt") as file:
        maxLen = max(maxLen,len(file.read()))

for i in range(numberOfSenders):
    startSenderThread = threading.Thread(target = startSender , args = (f"dataFiles/file{(i+1)}.txt",maxLen))
    senders.append(startSenderThread)
    startSenderThread.start()
    # print(f'inside thread {i+1}')

for i in range(numberOfSenders):
    senders[i].join()

print("Sending finished...")
print("Connection closed...")
