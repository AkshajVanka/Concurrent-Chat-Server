import socket
import threading
import os
import random
import pickle

# Connection Data
host = '127.0.0.1'
port = 5500
DISCONNECT_MESSAGE = "!END"

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"[LISTENING] Server is listening on {host}")

#Saving message data into a file
if os.path.exists('PythonText.txt'):
    os.remove('PythonText.txt')
else:
    print("File doesn't exist")

if os.path.exists('PythonTextFull.txt'):
    os.remove('PythonTextFull.txt')
else:
    print("Full File doesn't exist")

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
keys = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            d=client.recv(2048)
            data=pickle.loads(d)
            message=data.get('message')
            msg=data.get('msg')
            posString=data.get('posString')

            pos=[]
            if len(posString)!=0:
                pos = list(map(int, posString.split()))
            
            # Removing And Closing Clients
            if msg == DISCONNECT_MESSAGE:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.pop(index)
                keys.pop(index)
                print(nickname," left!")
                break

            s=[]
            # New key
            y = random.randint(1, 64)
            index = clients.index(client)
            x = keys[index]
            for i in range(0, len(msg)):
                c = msg[i]
                if i in pos:
                    s.append(chr(ord(c)+x-y))
                else:
                    s.append(c)
            
            st="".join(s)

            f = open("PythonText.txt", "w")
            f.write(st)
            f.close()

            f = open("PythonTextFull.txt", "a")
            f.write(st)
            f.write('\nKey : ' + str(y)+'\n')
            f.close()

            f = open("PythonText.txt", "r")
            echoString = f.read()
            f.close()
            echoString=st
            s=[]
            for i in range(0, len(echoString)):
                c = echoString[i]
                if i in pos:
                    s.append(chr(ord(c)+y))
                else:
                    s.append(c)
            
            newMsg = "".join(s)

            name=(message.split(':')[0])
            newMessage = '{}: {}'.format(name, newMsg)

            # Broadcasting Messages
            broadcast(newMessage.encode('ascii'))
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.pop(index)
            keys.pop(index)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        conn, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        conn.send('NICK-ADMIN'.encode('ascii'))
        d=conn.recv(2048)
        data=pickle.loads(d)
        nickname = data.get('nickname')
        key = int(data.get('key'))

        nicknames.append(nickname)
        clients.append(conn)
        keys.append(key%64)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        conn.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(conn,))
        thread.start()

receive()