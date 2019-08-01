import hashlib

def md5_encrypt(plaintxt):
    m5=hashlib.md5()
    m5.update(plaintxt.encode('utf-8'))
    ciphertxt=m5.hexdigest()
    return ciphertxt