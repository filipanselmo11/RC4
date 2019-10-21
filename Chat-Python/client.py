import socket
import sys
import threading
import random
import string
from RC4 import RC4
import time
import server

HOST = 'localhost'
PORT = 50007
varGlobal = {
   "RC4Key": "",
   "EncRC4Key": "",
   "RC4_sent": False,
   "OutroRc4": "" 
}

#Criando o socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Enviando uma solicitação de conexão
try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("Client não pode conectar")
    sys.exit()
print("Tentando estabelecer conexão...")

class ThreadReceive(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
    
    def run(self):
        global varGlobal

        while(True):
            message_recu = self.connexion.recv(1024).decode("Utf8")
            rc4 = RC4()
            rc4.shuffle(str(varGlobal["OutroRc4"]))
            message = rc4.Crypt(message_recu)
            print("-->>> " +message)


class ThreadSend(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
    
    def run(self):
        global varGlobal
        count = 0
        while(True):
            if(varGlobal["RC4_sent"]):
                if(count == 0):
                    print("### You are connected")
                    count += 1
                message_emis = input()
                Rc4 = RC4
                Rc4.shuffle(varGlobal["RC4Key"])

                m = Rc4.Crypt(message_emis)
                self.connexion.send(m.encode("Utf8"))


varGlobal["Rc4Key"] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

th_R = ThreadReceive(mySocket)
th_E = ThreadReceive(mySocket)

th_E.start()