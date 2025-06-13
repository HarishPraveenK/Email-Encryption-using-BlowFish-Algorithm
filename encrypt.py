from Crypto.Cipher import Blowfish
import base64

SECRET_KEY = b"Secret!"

def pad_message(message):
    pad_len = 8 - (len(message) % 8)
    return message + chr(pad_len) * pad_len

def unpad_message(message):
    pad_len = ord(message[-1])
    return message[:-pad_len]

def encrypt_msg(message):
    cipher = Blowfish.new(SECRET_KEY, Blowfish.MODE_ECB)
    padded_message = pad_message(message)
    encrypted = cipher.encrypt(padded_message.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_msg(encrypted_msg):
    cipher = Blowfish.new(SECRET_KEY, Blowfish.MODE_ECB)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_msg)).decode()
    return unpad_message(decrypted)
