import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[-1:])]


class AESC:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = base64.b64encode(pad(raw).encode('utf8'))
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))