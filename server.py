#codes for server
#a lot of import
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from datetime import datetime
from time import sleep

#a function that deals with every new member participating in the group chat
def accept_connect():
    while True:
        client, client_ip = SERVER.accept()
        private[client]=0       
        client.send(bytes("Please type your name and press enter!", "utf8"))
        client_name = client.recv(BUFSIZ).decode("utf8")
        byte=bytes(client_name, "utf8")
        #record each client socket and the user's name
        clients[client]=[byte,client_name]
        ips[client] = client_ip
        print("%s has connected and the user's name is %s." % (client_ip,client_name))
        #create multiple threads to represent server and serve each client.
        Thread(target=client_massage_handle, args=(client,clients,private)).start()
        
#a function that deals with receiving and sending of messages
def client_massage_handle(client,clients,private):  # take client socket as argument.
    flag2=0
    welcome = ('server:(Welcome %s! \nIf you want to quit, type {quit} to exit.)\n)' % clients[client][1])
    client.send(bytes(welcome, "utf8"))
    sleep(0.2)
    #the instructions of chatroom
    rule1 = ('(If you want to have private talk,please type {private})'% clients[client])
    client.send(bytes(rule1, "utf8"))
    sleep(0.2)
    rule2 = ('(If you want to quit private talk,please type {over})\n'% clients[client])
    client.send(bytes(rule2, "utf8"))
    sleep(0.2)
    rule3 = ('(If you want to decode,please type the correct code.)\n'% clients[client])
    client.send(bytes(rule3, "utf8"))
    sleep(0.1)
    massage = ("server:(%s has joined the chat.You can start to connect with this user\n)" % clients[client][1])
    broadcast(bytes(massage, "utf8"),flag2,clients,client )
    flag2=0
    while True:
        flag=0
        msg = client.recv(BUFSIZ)
###hndle the situation that the user wants to leave the chatroom
        if msg == bytes("{quit}", "utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            name=clients[client][1]
            del clients[client]
            broadcast((bytes("server: %s has left the chat"% name), "utf8"),flag2,clients,client,clients[1])
            break
###following code is to handle the user who wants to have private talk with other user.
        elif msg == bytes("{private}", "utf8"):
            #server send message to ask the user who wants to have private talk with other user.
            client.send(bytes("(Who do you want to connect with?)", "utf8"))
            #server receive the user's name that the user wants to have private talk with.
            msg = client.recv(BUFSIZ)
            #search the corresponding socket in "clients" dictionary
            for sock in clients:
                flag=1
                if clients[sock][0]==msg:
                    #flag=0 means the user exists
                    flag=0
                    #private[] is a dictionary that share between all threads
                    #private[client] is like a flag and it will record the user status.whenever the user is in "private" status,the value of the flag will become 1
                    private[client]=1
                    #send message to the user that you want to connect with to ensure he/she ia willing to connect with
                    #be careful of the form that the user enter should meet the requirement.(you should type "space" between {Yes} and user's name)ex:{Yes} Henry
                    msg="(%s connect with you privately and please type({Yes} his/hername))" %clients[client][1]
                    sock.send(bytes(msg, "utf8"))
                    client.send(bytes("(If you want to quit private talk,please type {over})", "utf8"))
                    while True:
                        # to enter another status is broadcast function
                        flag2=1
                        #private_clients is another dictionaery to record the users who are in "private" status
                        private_clients={}
                        msg = client.recv(BUFSIZ)
                        #private[sock]==0 means the user already left the "private" status
                        if private[sock]==0:
                            client.send(bytes("(server:the user doesn't want to connect with you!)", "utf8"))
                            break
                        #leave the "private status" and turn the value of flag to 0
                        if msg==bytes("{over}", "utf8"):
                            private[client]=0
                            break
                        private_clients[sock]=clients[sock]
                        private_clients[client]=clients[client]
                        broadcast(msg,flag2,private_clients,client,str(clients[client][1])+": ")
            #flag==1 means the user doesn't exist
            if flag==1:
                client.send(bytes("(The user doesn't exist!)", "utf8"))
###following code is to handle the situation when other user wants to have private talk with you, how can you reject or accept him/her. 
        # if you enter {Yes}, that means you are willing to connect with the user
        elif msg[:5] == bytes("{Yes}", "utf8"):
            private[client]=1
            # to search the user that wants to connect with you in "clients" dictionary
            sock_name=msg[6:]
            for sock in clients:
                if clients[sock][0]==sock_name:
                    while True:
                        msg = client.recv(BUFSIZ)
                        # to enter another status is broadcast function
                        flag2=1
                        #private_clients is another dictionaery to record the users who are in "private" status
                        private_clients={}
                        #private[sock]==0 means the user already left the "private" status
                        if private[sock]==0:
                            client.send(bytes("(server:the user doesn't want to connect with you!)", "utf8"))
                            break
                        #leave the "private status" and turn the value of flag to 0
                        if msg==bytes("{over}", "utf8"):
                            private[client]=0
                            break
                        print(sock)
                        private_clients[sock]=clients[sock]
                        private_clients[client]=clients[client]
                        broadcast(msg,flag2,private_clients,client,str(clients[client][1])+": ")
        #finish sending a file or photo
        elif msg[:10] == bytes('[===] 100%','utf8'):
            flag2=0
            #print(msg)
            sleep(0.2)
            broadcast(msg,flag2,clients,client) 
        #start sending a file
        elif msg[:5] == bytes("#####", "utf8") or flag2==2:
            flag2=2
            broadcast(msg,flag2,clients,client)
        #start sending a photo
        elif msg[:5] == bytes("?????", "utf8") or flag2==2:
            flag2=2
            broadcast(msg,flag2,clients,client)
###"commom" status which broadcasts the message to all the member in the chat room
        else:
            time = '     ---'+datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            time = bytes(time, "utf8")
            msg+=time
            broadcast(msg,flag2,clients,client,str(clients[client][1])+": ")
            
#a function that deals with sending of messages
def broadcast(msg,flag2,clients,client,prefix="",):
    #"common" status
    if flag2==0:
        for sock in clients:
            sock.send(bytes(prefix, "utf8")+msg)
    #"private" status
    if flag2==1:
        for sock in clients:
            sock.send(bytes(prefix, "utf8")+msg)
            sleep(0.001)
    #"image sending and file sending" status
    if flag2==2:
        for sock in clients:
            if sock!=client:
                sock.send(msg)
                sleep(0.001)
clients = {}
ips = {}
private={}
file={}
#please enter you ipv4
HOST = ''
#please enter the port number
#the number should be larger than 1024
PORT = 
ADDR = (HOST, PORT)
BUFSIZ = 1024
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connect)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
