import binascii
import sys, os, hashlib, time, base64
class RC4():
    def __init__(self, chaveStr, TamChave=16):
        self.TamChave = TamChave
        self.chaveStr = chaveStr or 'none_key'
        #chave = hashlib.md5(self.chaveStr).encode('utf-8').hexdigest()
        chave = hashlib.md5(self.chaveStr.encode('utf-8')).hexdigest()
        self.chaveA = hashlib.md5(chave[0:16].encode('utf-8')).hexdigest()
        self.chaveB = hashlib.md5(chave[16:32].encode('utf-8')).hexdigest()
        self.chaveC = ''

    def cifrar(self, data):
        self.chaveC = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[(32-self.TamChave):32]
        data = '0000000000' + hashlib.md5((data + self.chaveB).encode('utf-8')).hexdigest()[0:16] + data
        result = self.RC4(data)
        return self.chaveC + base64.b64encode(result)
    
    def decifrar(self, data):
        self.chaveC = data[0:self.TamChave]
        data = base64.b64decode(data[self.TamChave])
        result = self.RC4(data)
        if(result[0:10] == '0000000000' or int(result[0:10]) - int(time.time()) > 0) and result[10:26] == hashlib.md5(result[26:] + self.chaveB).hexdigest()[0:16]:
            return result[26:]
        else:
            return None
        
    def RC4(self, data):
        tamData = len(data)
        result = ''
        box = list(range(256))
        chaveAleatoria = []
        cifraChave = self.chaveA + hashlib.md5((self.chaveA + self.chaveC).encode('utf-8')).hexdigest()
        tamChave = len(cifraChave)
        for i in range(255):
            chaveAleatoria.append(ord(cifraChave[i % tamChave]))
        for i in range(tamData):
            a = j = 0
            a = (a + 1) % 256
            j = (j + box[a]) % 256
            box[a], box[j] = box[j], box[a]
            result += chr(ord(data[i])^ (box[(box[a] + box[j]) % 256]))
        return result


if __name__ == '__main__':
        rc4 = RC4('jianan')
        data = 'Ola script, vai se lascar'
        print(data)
        message = rc4.cifrar(data)
        print(message)
        message = rc4.decifrar(message)
        print(message)
