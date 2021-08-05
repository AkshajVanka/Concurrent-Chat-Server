import socket
import threading
import pickle

# Choosing Nickname
nickname = input("Choose your nickname: ")
# Accepting the 1st encryption key from the client
fl = False
key = ""
x=0
while not fl:
    try:
        key = input("Enter the encryption key: ")
        check = int(key)
    except ValueError:
        print("In-Valid Input (Enter a number)")
        continue
    fl = True

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5500))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK-ADMIN' Send nickname and key
            message = client.recv(1024).decode('ascii')
            if message == 'NICK-ADMIN':
                data={"nickname":nickname, "key":key}
                d=pickle.dumps(data)
                client.send(d)
            else:
                print(message)
        except:
            # Close Connection When Error
            print("Ended connection/An error has occured.")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        msg=input()
        if msg == '!END':
            client.close()
            message = '{}: {}'.format(nickname, msg)
            data={"message": message, "msg": msg, "posString":""}
            d=pickle.dumps(data)
            client.send(d)
            break
        st=[]
        pos=[]
        x= int(key)%64
        for i in range(len(msg)):
            c = msg[i]
            if c.isalpha():
                st.append(chr(ord(c)-x))
                pos.append(str(i)+" ")
            else:
                st.append(c)
        encodedString = ''.join(st)
        posString = "".join(pos)
        message = '{}: {}'.format(nickname, encodedString)
        data={"message": message, "msg": encodedString, "posString": posString}
        d=pickle.dumps(data)
        client.send(d)

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()