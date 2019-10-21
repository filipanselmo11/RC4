from tkinter import *
import socket
from threading import Thread
from random import *
import random
import sys
import binascii

class RC4:
    S = []
    p = q = None
    chave = ""

    def __init__(self):
        self.chave = self.convertKey()

    def KSA(self):
        self.p = 0
        self.q = 0
        tamChave = len(self.chave)

        self.S = range(256)
        j = 0
        for i in range(0,256):
            j = (j + self.S[i] + ord(self.chave[i % tamChave])) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        
    def PRGA(self):
        self.p = (self.p + 1) % 256
        self.q = (self.q + self.S[self.p]) % 256
        self.S[self.p], self.S[self.q] = self.S[self.q], self.S[self.p]

        return self.S[(self.S[self.p] + self.S[self.q]) % 256]
    
    def encrypt(self, textoPlano):
        self.KSA()
        return "".join("%02X" % (ord(c) ^ self.PRGA()) for c in textoPlano)

    def decrypt(self, cipher):
        self.KSA()
        listaByte = []
        for i in range(0, len(cipher), 2):
            byte = cipher[i:i+2]
            listaByte.append(int(byte, 16))
        return "".join([chr(byte ^ self.PRGA()) for byte in listaByte])
    
    def convertKey(self):
        return[ord(c) for c in self.chave]


class Receive():
    def __init__(self, servidor, messagesLog):
        self.servidor = servidor
        self.messagesLog = messagesLog

        while(True):
            try:
                text = self.servidor.recv(1024)
                


'''
if(__name__ == '__main__'):
    rc4 = RC4()
    chave = input('Sua chave: ')
    rc4.convertKey()
    while(True):
        message = input('Sua mensagem: ')
        print(message)
        E = rc4.encrypt(message)

        print("Mensagem cifrada: ", E)
        M = rc4.decrypt(message)
        print("Mensagem decifrada: ", M)
'''