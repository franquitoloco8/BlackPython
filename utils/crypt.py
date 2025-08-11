from cryptography.fernet import Fernet

class AESEncryptor:
    def __init__(self, key):
        self.key = Fernet.generate_key() if key == "SUPER_SECRET_KEY" else key.encode()
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data).decode()
