from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AESCrypt:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        text = self.pad(text)
        cryptor = AES.new(self.key, self.mode, self.iv)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return self.unpad(bytes.decode(plain_text).rstrip('\0'))

if __name__ == "__main__":
    test_str = "abcde12345"
    AES_KEY = b'1234123412ABCDEF'
    AES_IV = b'ABCDEF1234123412'
    crypt = AESCrypt(AES_KEY, AES_IV)
    cry_str = crypt.encrypt(test_str)
    decy_str = crypt.decrypt(cry_str)
    print("cry_str:{0}".format(cry_str.decode()))
    print("decy_str:{0}".format(decy_str))
