from cryptography.fernet import Fernet
from django.conf import settings

def encrypt_data(data):
    key = settings.ENCRYPTION_KEY.encode()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data):
    key = settings.ENCRYPTION_KEY.encode()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
    return decrypted_data.decode()
