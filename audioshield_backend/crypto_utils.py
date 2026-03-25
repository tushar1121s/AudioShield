import librosa
import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Audio file se 256-bit Key nikalne ka function
def generate_key_from_audio(audio_path):
    # Audio load karna
    y, sr = librosa.load(audio_path, sr=None)
    # Audio data ko bytes mein convert karke hash karna
    audio_bytes = y.tobytes()
    return hashlib.sha256(audio_bytes).digest()

# Data ko encrypt karne ka function
def encrypt_data(data, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12) 
    return nonce + aesgcm.encrypt(nonce, data, None)