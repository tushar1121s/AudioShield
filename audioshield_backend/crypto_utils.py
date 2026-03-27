import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Seedha bytes se key banayega
def generate_key_from_bytes(audio_bytes):
    return hashlib.sha256(audio_bytes).digest()

def encrypt_data(data, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext

def decrypt_data(encrypted_data, key):
    aesgcm = AESGCM(key)
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)