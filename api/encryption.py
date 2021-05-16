import base64
from Crypto.Cipher import AES
from Crypto import Random

SECRET_KEY = b'Xp2s5v8y/A?D(G+KbPeShVmYq3t6w9z$'


class AESCipher:

    @classmethod
    def encrypt_string(cls, raw):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))

    @classmethod
    def decrypt_string(cls, enc):
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode("utf-8")
