import secrets
import hashlib
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

g = 3
p = 0xf66a1d0b27dd06c0c24b43030fa04963517942744a68004da3b01b6a999783e8001a4eb8182202c805b20e40c22fbbf05156aca964cb355d8248d9ac2547f307a5bdaaac0b29a06f3e1f11d0bb9985564887ae686e8726bf43f75ea1d99a26227f5daaac0b29a06f3e1f11d0bb9985564887ae686e8726bf43f75ea1d99a26227f507e5fb40d8d3e5d98d2c1f61e78e6098e232c7224d0d666d3231c7a56cb3c4d407e5fb40d8d3e5d98d2c1f61e78e6098e232c7224d0d666d3231c7a56cb3c4d402df1dd6112aba6fc2a85f271328de1c4e88edfa833bd5ddf829b5a6ddad677802df1dd6112aba6fc2a85f271328de1c4e88edfa833bd5ddf829b5a6ddad677

class Server():
    def __init__(self, port=1337):
        self.port = port
        self.sKE = ShiftyKeyExchange(g, p)
        self.y_server = self.sKE.calculate_y()
        self.y_client = 0
        self.IV = "84ba189a9afdeb02"
        self.key = "421337427"
        
    def run(self):
        input("Press <Enter> to start ...")
        print("\x1b[2J\x1b[H")
        print("Here's my y = {0}\n\n".format(self.y_server))
        self.y_client = int(input("Give me your y please: "))
        self.key = str(self.sKE.calculate_key(self.y_client))
        self.iv = self.key[0:16]
        self.encrypt()

    def encrypt(self):
        key = bytes(hashlib.md5(bytes(self.key, "utf-8")).hexdigest(), "utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv=bytes(self.iv, "utf-8"))
        cipher_text_bytes = cipher.encrypt(pad(b"The Advanced Encryption Standard (AES), also known by its original name Rijndael, is a specification for the encryption of electronic data established by the U.S. National Institute of Standards and Technology (NIST) in 2001.", AES.block_size))
        print(b64encode(cipher_text_bytes))
        
class ShiftyKeyExchange():
    def __init__(self, g, p):
        self.g = g
        self.p = p
        self.x = self.get_random_x()

    def get_random_x(self):
        return secrets.SystemRandom().randint(g, p-2)
    
    def calculate_y(self):
        return (self.g * self.x) % self.p

    def calculate_key(self, y):
        return (y * self.x) % self.p

if __name__ == "__main__":
    server = Server()
    server.run()
        
        


    
