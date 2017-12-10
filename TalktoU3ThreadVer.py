import socket
import sys
import threading

#TA server IP&port
#host : 128.199.83.36
#port : 34260

class mySocket:
    
    def __init__(self,host,port):
        self.ThreadStart(host,port)
    
    def heartandauthen(self,host,port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host,port))  
        self.authen()
        self.status()
        self.friend = self.s.recv(4096).decode().split('\n')
        self.printfriend()
        self.beat()
    
    def listen(self):
        listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenSock.bind((self.UserIP,self.UserPort))
        listenSock.listen(1)
        while 1:
            client_socket, client_address = mySocket.accept()
            T = threading.Thread(target=handle_client, args=(client_socket, client_address))
            T.daemon = True
            T.start()
    
    def handle_client(self,client_socket,client_address):
        endmsg = "To end connection please type 'end' \n"
        client_socket.send(bytes(endmsg),'uft-8')
        print(endmsg)
        recvT = threading.Thread(target=recv_client,args=(client_socket,client_address))
        recvT.daemon = True
        recvT.start()

        sendT = threading.Thread(target=send_client, args=(client_socket,client_address))
        sendT.daemon = True
        sendT.start()

    def send_client(self,client_socket,client_address):
        while 1:
            Userinput  = input()
            if(Userinput == 'end'):
                print("closing connection with : "+ client_address)
                client_socket.shutdown(socket.SHUT_WR)
            else:
                client_socket.send(bytes(Userinput,'utf-8'))

    def recv_client(self,client_socket,client_address):
            while 1:
                data = self.s.recv(4096).decode()
                if not data:
                    client_socket.shutdown(socket.SHUT_WR)
                    break
                elif data.split('\n')[0] == 'end\r':
                    print('End Connection with : '+client_address)
                    client_socket.shutdown(socket.SHUT_WR)
                    break
                else :
                    print("Your Friend '"+client_address+"' : "+data)

    def beat(self):
        while 1:
            if self.s.recv(4096).decode() == "Hello " + self.Userid :
                self.Sending("Hello Server")
    
    def authen(self):
        self.Userid = '5809680092'
        self.Password = '0092'
        self.UserPort = 55555
        self.UserIP = socket.gethostbyname(socket.gethostname())
        authenmsg = 'USER:'+ self.Userid +"\nPASS:"+ self.Password + "\nIP:" + self.UserIP + \
        "\nPORT:" + str(self.UserPort) +"\n"
        self.Sending(authenmsg)
    
    def status(self):
        status = self.s.recv(4096).decode().strip(" \n")
        if status == '200 SUCCESS':
            print('Authentication Successed\n')
        else:
            print('Authentication Denied\n')
            sys.exit(-1)

    def Sending(self,msg):
        self.s.send(bytes(msg,'utf-8'))

    def printfriend(self):
        print('Friend List\n')
        for friendl in self.friend:
            if friendl != 'END' and friendl != '':
                result = friendl+" (Status : "
                friendline = friendl.split(':')
                if(friendline[1] == '-1'):
                    print(result + 'offline)\n')
                else:
                    print(result + 'online)\n')

    def ThreadStart(self,host,port):
        threading.Thread(target = self.heartandauthen(host,port)).start()
        threading.Thread(target = self.listen).start()
        # threading.Thread(target = self.conn).start()

#starting point
Starto = mySocket('128.199.83.36',34260)