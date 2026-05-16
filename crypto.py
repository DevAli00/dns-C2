from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt(data: str, key: bytes) -> bytes:
    nonce = os.urandom(12)        # 12 random bytes, different every time
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data.encode(), None)
    return nonce + ciphertext     # prepend nonce so decrypt can find it

def decrypt(data: bytes, key: bytes) -> str:
    nonce = data[:12]             # first 12 bytes are the nonce
    ciphertext = data[12:]        # rest is the actual ciphertext + auth tag
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode()

def generate_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)  # 32 random bytes