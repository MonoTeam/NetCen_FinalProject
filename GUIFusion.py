from tkinter import *
from tkinter import *
from tkinter import messagebox 
import socket
import sys
import threading

class TalktoUIMain(Frame):
    def __init__(self,Tkin):
        self.Tkin = Tkin
        self.Tkin.title("Net-CEN Project")
        #User Section
        self.Username = Label(Tkin,text="Username: ")
        self.Username.grid(row=1)

        self.UsernameInput = Entry(Tkin)
        self.UsernameInput.grid(row=1,column=1)

        self.Pass = Label(Tkin,text="Password: ")
        self.Pass.grid(row=2)

        self.PassInput = Entry(Tkin)
        self.PassInput.grid(row=2,column=1)

        self.ip = socket.gethostbyname(socket.gethostname())
        self.IPLabel = Label(Tkin,text="Your IP is : "+self.ip)
        self.IPLabel.grid(row=3,columnspan=2,sticky=N+W+S+E)

        self.Port = Label(Tkin,text="Port : ")
        self.Port.grid(row=4)

        self.PortInput = Entry(Tkin)
        self.PortInput.grid(row=4,column=1)

        self.loginBtn = Button(Tkin,text="Login",command=self.login)
        self.loginBtn.grid(row = 5,columnspan=2)

        self.f = Label(Tkin,text="Connect With Friend")
        self.f.grid(row = 8,columnspan=2,sticky=N+W+S+E)

        self.fip = Label(Tkin,text="Friend's IP : ")
        self.fip.grid(row = 9)
        self.fp = Label(Tkin,text="Friend's Port : ")
        self.fp.grid(row=10)
        #Friend section
        self.fipInput = Entry(Tkin)
        self.fipInput.grid(row=9,column=1)
        self.fpInput = Entry(Tkin)
        self.fpInput.grid(row=10,column=1)
        self.loginBtn = Button(Tkin,text="Connect To friend",command=self.CTF)
        self.loginBtn.grid(row=11,columnspan=2)
        
        self.FA = Frame(Tkin)
        self.FA.grid(row=7,columnspan=2,sticky=N+W+S+E)
        self.scrollb = Scrollbar(self.FA,orient=VERTICAL)
        self.list = Listbox(self.FA,yscrollcommand=self.scrollb.set,height=30,width=50)
        #self.list.grid(row=10,columnspan=2,sticky=N+W+S+E)
        self.scrollb.config(command=self.list.yview)
        self.scrollb.pack(side=RIGHT,fill=Y)

        self.list.pack()

    def login(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('128.199.83.36',34260))
        authenmsg = 'USER:'+ self.UsernameInput.get() +"\nPASS:"+ self.PassInput.get() + "\nIP:" + self.ip + "\nPORT:" + self.PortInput.get() +"\n"
        self.Sending(authenmsg)
        self.status()
        self.getfriend()
        threading.Thread(target = self.beat).start()
        threading.Thread(target = self.listenS).start()
        self.UsernameInput.config(state='disable')
        self.PassInput.config(state='disable')
        self.PortInput.config(state='disable')

    def status(self):
        try:
            status = self.s.recv(4096).decode().strip(" \n")
        except UnicodeDecodeError:
            raise UnicodeDecodeError
        except TypeError:
            raise TypeError

        if status == '200 SUCCESS':
            messagebox.showinfo('Pass','Authentication Successed')
        else:
            messagebox.showinfo('Fail','Authentication Denied')

    def getfriend(self):
        self.friend = self.s.recv(4096).decode().split('\n')
        self.friendList = []
        for friendl in self.friend:
            if friendl != 'END' and friendl != '':
                result = friendl+" (Status : "
                friendline = friendl.split(':')
                if(friendline[1] == '-1'):
                    result+='offline)\n'
                else:
                    result+='online)\n'
                self.list.insert(END,result)
    def listenS(self):
        listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenSock.bind((self.ip,(int)(self.PortInput.get())))
        listenSock.listen(1)
        while 1:
            (client_socket, client_address) = listenSock.accept()
            messagebox.showinfo('IT\'S COMING!!','You got connection')
            self.Tkin.withdraw()
            datagram = {
              "consoc" : client_socket,
              "port" : client_address
            }
            Chatter = ChatUI(datagram)

    def beat(self):
        while 1:
            sendmsg = "Hello " + self.UsernameInput.get()
            servermsg = self.s.recv(4096).decode()
            if sendmsg == servermsg:
                self.Sending("Hello Server")
    
    def CTF(self):
        self.ctfs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ctfs.connect((self.fipInput.get(),int(self.fpInput.get())))
        datagram = {
              "consoc" : self.ctfs,
              "port" : int(self.fpInput.get())
         }
        self.Tkin.withdraw()
        self.chatter = ChatUI(datagram)

    def Sending(self,msg):
        try:
            self.s.send(bytes(msg,'utf-8'))
        except BrokenPipeError:
            raise BrokenPipeError

class ChatUI():
    def __init__(self,datagram):

        self.base = Tk()
        self.base.title("bra bra")
        self.datagram = datagram
        self.soc  = datagram['consoc']
        self.port = datagram['port']
        self.base.geometry("400x500")
        threading.Thread(target=self.recieveMessage,args=(self.soc,self.port)).start()
        self.base.resizable(width=FALSE, height=FALSE)

        self.ChatLog = Text(self.base, bd=0, bg="white", height="8", width="40", font="Arial",)
        self.ChatLog.config(state=DISABLED)

        self.scrollbar = Scrollbar(self.base, command=self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        self.EntryBox = Entry(self.base, bd=0, bg="white")
        self.EntryBox.config(state=NORMAL)
        self.SendButton = Button(self.base, font=30, text="Send", width="12", height=5,
                    bd=0, bg="#FFBF00", activebackground="#FACC2E",command=self.Send)
        
        self.scrollbar.place(x=376,y=6, height=386)
        self.ChatLog.place(x=6,y=6, height=386, width=370)
        self.EntryBox.place(x=145, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=90)
        
        self.base.mainloop()
    
    def Send(self,event=None):
        msg=self.EntryBox.get()+'\n'
        try:
            self.soc.send(bytes(msg,'utf-8'))
        except BrokenPipeError:
        	raise BrokenPipeError
        if msg != "":
            self.EntryBox.delete(0, 'end')
            self.ChatLog.config(state=NORMAL)
            self.ChatLog.insert('end','You : ' + msg)
            self.ChatLog.config(state=DISABLED)
            self.ChatLog.see(END)

    def recieveMessage(self, sock, address):
        while True:
            try:
                recv_msg = sock.recv(4096).decode()
                print(recv_msg)
            except UnicodeDecodeError:
                raise UnicodeDecodeError
            except TypeError:
                raise TypeError

            self.ChatLog.config(state=NORMAL)
            self.ChatLog.insert('end',"friend : " + recv_msg + "\n")
            self.ChatLog.config(state=DISABLED)
            self.ChatLog.see(END)
            
Tkin = Tk()
starto = TalktoUIMain(Tkin)
Tkin.mainloop()
