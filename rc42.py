import codecs
import os

mod = 256

def ksa(chave):
    S = list(range(mod))
    j = 0
    tamChave = len(chave)
    for i in range(mod):
        j = (j + S[i] + chave[i % tamChave]) % mod
        S[i], S[j] = S[j], S[i]
    return S


def prga(S):
    i = j = 0
    while(True):
        i = (i + 1) % mod
        j = (j + S[i]) % mod
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % mod]
        yield K

def rc4(chave):
    S = ksa(chave)
    return prga(S)

def logica(chave, texto):
    chave = [ord(c) for c in chave]
    chave_stream = rc4(chave)
    res = []
    for c in texto:
        val = ("%02X" % (c ^ next(chave_stream)))
        res.append(val)
    return ''.join(res)

def cifrar(chave, textoPlano):
    textoPlano = [ord(c) for c in textoPlano]
    return logica(chave, textoPlano)

def decifrar(chave, textoCifrado):
    textoCifrado = codecs.decode(textoCifrado, 'hex_codec')
    res = logica(chave, textoCifrado)
    return codecs.decode(res, 'hex_codec')

def main():
    while(True):
        #print("Usuário 1")
        chave = os.urandom(16)
        mensagem = input('Informe a mensagem: ')
        print('Mensagem: ', mensagem)
        print("Mensagem Enviada \n")
        #print("Usuario 2")
        print("Mensagem Recebida")
        cfr = cifrar(chave, mensagem)
        print("Mensagem cifrada: ", cfr)
        dfr = decifrar(chave, cifrar)
        print("Mensagem decifrada: ", dfr)
        print("\n")


if __name__ == '__main__':
    main()