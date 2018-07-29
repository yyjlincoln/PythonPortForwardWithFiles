import socket
from socket import *
import time
import random
import _thread
import os
COMMANDUSED=[]
content=b''
lastcontent=b''
class server:
    Sock=None
    work='H:\\Sp\\'
    def __init__(self,forward=('localhost',80)):
        print('Mode:Server. File->Socket(Connect):',forward[0],forward[1])
        self.addr=forward
        Soc=self.Sock=socket(AF_INET,SOCK_STREAM)
        self.Datain=self.work+'sp'+str(forward[1])+'.datain'
        self.Dataout=self.work+'sp'+str(forward[1])+'.dataout'
        self.Status=self.work+'sp'+str(forward[1])+'.status'
        with open(self.Datain,'w') as f:
            f.write('')
        with open(self.Dataout,'w') as f:
            f.write('')
        with open(self.Status,'w') as f:
            f.write('')        
        _thread.start_new(self.connection_monitor,(self.Status,))
    
    def connection_monitor(self,file):
        with open(file,'r') as f:
            content=f.read()
            lastcontent=content
            while True:
                while content==lastcontent:
                    f.seek(0,0)
                    content=f.read()
                if content!=b'':
                    print('Status Change Detected')
                    command=content
                    if command in COMMANDUSED:
                        lastcontent=content
                        continue
                    #print('Command',command)
                    COMMANDUSED.append(command)
                    if command[:9]=='CONNECT//':
                        R=int(command[9:])
                        print('Connecting, R = ',R)
                        R=R*2+1
                        print('Calculated R = ',R)
                        print('Writing Status...')
                        write_status(self.Status,'CONFIRM//'+str(R))
                        print('Connection Established.')
                        Soc=self.Sock
                        Soc.connect(self.addr)
                        _thread.start_new(socket_to_file,(self.Dataout,Soc))
                        _thread.start_new(file_to_socket,(self.Datain,Soc))
                        print('Threads started.')
                lastcontent=content


class client:
    content=b''
    lastcontent=b''
    Sock=None
    R=random.randint(1,20000)
    RC=R*2+1
    work='H:\\Sp\\'
    def __init__(self,forward=('localhost',80),local=('localhost',81)):
        print('Mode:Client. Localsocket->File. Target:',forward[0],forward[1],'Server on local:',local[0],local[1])
        Soc=self.Sock=socket(AF_INET,SOCK_STREAM)
        Soc.bind(local)
        Soc.listen(1)
        self.Datain=self.work+'sp'+str(forward[1])+'.dataout'
        self.Dataout=self.work+'sp'+str(forward[1])+'.datain'
        self.Status=self.work+'sp'+str(forward[1])+'.status'
        with open(self.Datain,'w') as f:
            f.write('')
        with open(self.Dataout,'w') as f:
            f.write('')
        with open(self.Status,'w') as f:
            f.write('')        
        _thread.start_new(self.socket_listen,(Soc,))
    
    def socket_listen(self,socketobject):
        while True:
            so,addr=socketobject.accept()
            write_status(self.Status,'CONNECT//'+str(self.R))
            _thread.start_new(socket_to_file,(self.Dataout,so))
            _thread.start_new(file_to_socket,(self.Datain,so))
            _thread.start_new(self.connection_monitor,(self.Status,))
    
    def connection_monitor(self,file):
        with open(file,'r') as f:
            content=f.read()
            lastcontent=content
            while True:
                while content==lastcontent:
                    f.seek(0,0)
                    content=f.read()
                if content!=b'':
                    print('Status Change Detected')
                    command=content
                    #print('Command',command)
                    if command in COMMANDUSED:
                        lastcontent=content
                        continue
                    COMMANDUSED.append(command)
                    if command=='CONFIRM//'+str(self.RC):
                        print('Conencted.')
                        _thread.exit()
                lastcontent=content
        
def file_to_socket(file,socketobject):
    global content, lastcontent
    with open(file,'rb') as f:
        content=f.read(509600)
        lastcontent=b''
        while True:
            time.sleep(0.2)
            print('Waiting for file change')
            while content==lastcontent:
                #print(content,lastcontent)
                f.seek(0,0)#移到文件头,再读
                content=f.read()
            #print(content,lastcontent)
            #print(len(content),len(lastcontent))
            if content!=b'':
                print('File Change Detected.')
                try:
                    socketobject.send(content)
                    print('Socket_to_file: Successfully Sent Data, Length',len(content))
                    #print('Successfully sent, Data:',content)
                except:
                    print('Socket_to_file: Failed to send data, Length',len(content))
                    #print('Failed to send socketobject.send(), Data:',content)
                    print('Socket_to_file: Close Connection...')
                    try:
                        socketobject.close()
                    except:
                        print('Socket_to_file: Failed to close connection..')
                    print('Socket_to_file: Terminated. Exit Thread.')
                    _thread.exit()
            lastcontent=content

def socket_to_file(file,socketobject):
    while True:
        time.sleep(0.2)
        try:
            content=socketobject.recv(509600)
            #print('Content Recv')
            print('Content Recv')
        except:
            _thread.exit()
        if content!=b'':
            with open(file,'wb') as f:
                f.write(content)
                #print(content)
            #    print('Content Written')
                print('Content Written, Length',len(content))
        else:
            #print('Blank Content. Connection Reset?')
            #print('Close Connection...(S2F)')
            try:
                socketobject.close()
            except:
                #print('Failed to close connection.(S2F)')
                print(2)
            _thread.exit()

def write_status(file,status):
    with open(file,'w') as f:
        f.write(status)
