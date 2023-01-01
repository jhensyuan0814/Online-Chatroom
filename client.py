#codes for client
#a lot of import
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import*
import tkinter
import random
import string
import sys
from tkinter import filedialog
from time import sleep
from random import choice
from vpython import *
import datetime
import time

pos, angle = vector(0, 0, 0), 0
#the welcome page created with vpython
scene = canvas(width=400, height=400, range = 20, background=color.black)
ball = sphere(radius = 10.0, texture=textures.earth,emissive=True )
msg =text(text = 'Welcome to Python Mineline--a global group chat', pos = vec(-14.8,15,0),depth=-0.5)

t=100
#t counts from 100 to 0, and when t==0, the while loop breaks.
#Then you can start to use python miniline
while True:
    t-=1
    rate(1000)
    time.sleep(0.001)
    #the welcome page which is labeled with current time
    msg = label(text='\r %s'% datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,pos=vec(0,12,0),end='')
    #the earth will rotate
    ball.rotate(angle=pi/6000, axis= vector(sin(angle),cos(angle),0), origin=pos)
    ball.pos = pos
    print('\r',t,'   ',end='')
    if t==0:
        break
        
#a function that can send file 
def send_file(event=None):
    #interface
    root = tkinter.Tk()
    root.withdraw()
    try:
        photo_path = filedialog.askopenfilename()

        f = open (photo_path, "rb")
        l = f.read(1024)
        #start sending the photo
        client_socket.send(bytes('#####', "utf8"))
        sleep(1)
        while (l):
            client_socket.send(l)
            l = f.read(1024)
        sleep(1)
        #finish sending the photo
        client_socket.send(bytes('[===] 100%', "utf8"))
    except:
        pass
 
#a function that can send photo
def send_photo(event=None):
    #interface
    root = tkinter.Tk()
    root.withdraw()
    try:
        photo_path = filedialog.askopenfilename()

        f = open (photo_path, "rb")
        l = f.read(1024)
        #start sending the photo
        client_socket.send(bytes('?????', "utf8"))
        sleep(1)
        while (l):
            client_socket.send(l)
            l = f.read(1024)
        sleep(1)
        #finish sending the photo
        client_socket.send(bytes('[===] 100%', "utf8"))
    except:
        pass
 
#a class that can calculate an equation
class number:
    #open a window that allows you to enter an equation
    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="please enter an equation").pack()
        self.e = Entry(top)
        self.e.pack(padx=20, pady=10)

        b = Button(top, text="OK", command=self.ok)
        b.pack(padx=10, pady=20)
    #you must press 'OK', otherwise the program will not run
    def ok(self):
        c=self.e.get()
        #print( "the value is",c)
        self.top.destroy()
        answer=Tk()
        #show the answer
        try:
            Button(answer, text="the answer is:%s"%eval(c)).pack()
        except:
            Button(answer, text="you use the calculator in a wrong way").pack()

#a function that can calculate an equation
#what you have done here won't be seen by others
def calculator():
    root = Tk()
    root.withdraw()
    d = number(root)
    root.wait_window(d.top)
    
#a function that deals with receiving of messages 16,3    
def receive():
    flag=0
    fileopen=0
    while True:
            msg = client_socket.recv(BUFSIZ)
            #print(msg[:5])
            
            #receiving a file
            if msg[:5] == bytes('#####', "utf8") or flag==1:
                if fileopen==1:
                    f=open(filename,"ab+") 
                if fileopen==0:
                    filename='d:\miniline_file%s.txt'% datetime.datetime.now().strftime('%Y%m%d %H%M%S')
                    f=open(filename,"ab+")
                    fileopen=1
                
                #start receiving the file
                if msg[:5]==bytes('#####', "utf8"):
                    f.write(msg[5:])
                    flag=1
                #finish receiving the file
                elif msg[:10] == bytes('[===] 100%','utf8'):
                    flag=0
                    fileopen=0
                #receiving the file
                else:
                    f.write(msg)
                    flag=1
                f.close()
                
            #receiving a photo
            elif msg[:5] == bytes('?????', "utf8") or flag==2:
                if fileopen==1:
                    f=open(filename,"ab+") 
                if fileopen==0:
                    filename='d:\miniline_image%s.jpg'% datetime.datetime.now().strftime('%Y%m%d %H%M%S')
                    f=open(filename,"ab+")
                    fileopen=1
                
                #start receiving the photo
                if msg[:5]==bytes('?????', "utf8"):
                    f.write(msg[5:])
                    flag=2
                #finish receiving the photo
                elif msg[:10] == bytes('[===] 100%','utf8'):
                    flag=0
                    fileopen=0
                #receiving the photo
                else:
                    f.write(msg)
                    flag=2
                f.close()
            elif flag==0:
                try:
                    msg = msg.decode("utf8")
                    msg_list.insert(tkinter.END, msg)
                except OSError:  #maybe the client has left the chat
                    break
            #print(flag)

#a function that deals with the sending of messages
def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

#a function that can thumb up
def good(event=None):  
    #randomly generate the message
    great1 = ['breathtaking', 'amazing', 'stunning', 'astounding', 'astonishing', 'awe-inspiring', 'stupendous', 'staggering', 'extraordinary', 'incredible', 'unbelievable', 'magnificent', 'wonderful', 'spectacular', 'remarkable', 'phenomenal', 'prodigious', 'miraculous', 'sublime', 'formidable', 'imposing', 'impressive']
    great2 = ['^o^','(*^_^*)','>﹏<','~^o^~','≧◇≦','∩_∩','☆_☆','‵▽′','^▽^','^@^','⊙o⊙']
    msg = choice(great1)+'!!! '+choice(great2)
    msg = msg.upper()
    client_socket.send(bytes(msg, "utf8"))

#a function that can quit chatting
def quit1(event=None):
    msg = '{quit}'
    client_socket.send(bytes(msg, "utf8"))
    #shut down the client's account
    client_socket.close()
    client_socket.destroy()

#a function that will be called when the window is closed
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

#a function that can encode messages
def encode_send(event=None):
    temp = my_msg.get()
    my_msg.set("")
    msg = ''
    #strip the punctuations
    for i in temp:
        if i not in string.punctuation:
            msg+=i
    msg = msg.lower()
    ans = Encode(msg,'03.py')
    client_socket.send(bytes(ans, "utf8"))
     
#a function that can decode messages
def decode_send(event=None):
    temp = my_msg.get()
    my_msg.set("")
    #default code:{0814}
    code = '{0814}'
    try:
        if code not in temp:
            raise ValueError
        else:
            temp = temp.replace(code,'')
        ans = Decode(temp,'06.py')
        client_socket.send(bytes(ans, "utf8"))
    #handle invalid input
    except ValueError:
        ans = 'I failed to decode! 〒.〒'
        client_socket.send(bytes(ans, "utf8"))

#a function that can encode words
def Encode(msg, dic_file):
    #the dictionary with code is saved in another py
    d = open(dic_file,'r')
    dd = eval(d.read())
    ans = ''
    for character in msg:
        if character in dd:
            ans += dd[character]
    return ans

#a function that can decode words
def Decode (msg, dic_file):
    #the dictionary with code is saved in another py
    d = open(dic_file,'r')
    dd = eval(d.read())
    temp,ans,count = '','',0
    for nums in msg:
        temp+=nums
        if temp in dd:
            ans+=dd[temp]
            temp ,count = '',0
        else:
            count+=1
    #handle invalid input
    if count!=0:
        raise ValueError
        return
    return ans

#open a tkinter window
top = tkinter.Tk()
#title of interface
top.title("Chatter")

messages_frame = tkinter.Frame(top)
#for the messages to be sent.
my_msg = tkinter.StringVar() 
my_msg.set("Type your messages here.")
#navigate through past messages.
scrollbar = tkinter.Scrollbar(messages_frame)
#following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=120, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

###interface and buttons setting
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
#a button that can send messages
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
#a button that can thumb up
like_button = tkinter.Button(top, text="Thumb up", command=good)
like_button.pack()
#a button that can quit chatting
quit_button = tkinter.Button(top, text="Quit", command= quit1)
quit_button.pack()
#a button that can encode messages
encode_button = tkinter.Button(top, text="Encode", command= encode_send)
encode_button.pack()
#a button that can encode messages
decode_button = tkinter.Button(top, text="Decode", command= decode_send)
decode_button.pack()
#a button that can send files
file_button = tkinter.Button(top, text='File', command=send_file)
file_button.pack()
#a button that can send photos
photo_button = tkinter.Button(top, text='Photo', command=send_photo)
photo_button.pack()
#a button that can calculate an equation
calculator_button = tkinter.Button(top, text='Calculator', command=calculator)
calculator_button.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)

#please enter you ipv4
HOST = '192.168.1.105'
#please enter the port number
#the number should be larger than 1024
PORT = 3333 
ADDR = (HOST, PORT)
BUFSIZ = 1024

#connect to the server
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
#starts GUI execution
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  
