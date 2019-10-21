import codecs

MOD = 256

def KSA(chave):
    S = list(range(MOD))
    j = 0
    tamChave = len(chave)
    for i in range(MOD): 
        j = (j + S[i] + chave[i % tamChave]) % MOD
        S[i], S[j] = S[j], S[i]
    return S


def PRGA(S):
    i = j = 0
    while(True):
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % MOD]
        yield K

    
def get_keystream(chave):
    S = KSA(chave)
    return PRGA(S)


def encrypt_logic(chave, texto):
    chave = [ord(c) for c in chave]
    chave_stream = get_keystream(chave)
    res = []
    for c in texto:
        val = ("%02X" % (c ^ next(chave_stream)))
        res.append(val)
    return ''.join(res)


def encrypt(chave, textoPlano):
    textoPlano = [ord(c) for c in textoPlano]
    return encrypt_logic(chave, textoPlano)


def decrypt(chave, cipherText):
    cipherText = codecs.decode(cipherText, 'hex_codec')
    res = encrypt_logic(chave, cipherText)
    return codecs.decode(res, 'hex_codec').decode('utf-8')

'''
def main():
'''
