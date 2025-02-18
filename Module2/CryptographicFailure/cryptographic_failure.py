from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

import os

# Hardcoded key (16 bytes for AES-128)
HARDCODED_KEY = b"1234567890abcdef"  # Hardcoded key is insecure

salt = os.urandom(16)

#vecteur d'initialisation
iv = os.urandom(16)

# Dériver la clé avec PBKDF2-HMAC et SHA-256
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1_000_000,
)

key = kdf.derive(HARDCODED_KEY)

# Encryption using PBKDF2 mode
def encrypt_file_pbkdf2(file_content):    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # padding (multiple de 16)
    pad_len = 16 - len(file_content) % 16
    file_content_padded = file_content + bytes([pad_len]) * pad_len
    encrypted_content = encryptor.update(file_content_padded) + encryptor.finalize()
    return encrypted_content

def decrypt_file_pbkdf2(encrypted_content):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    file_content_unpadded = decryptor.update(encrypted_content) + decryptor.finalize()
    # not padding added from encrypt
    pad_len = file_content_unpadded[-1]
    return file_content_unpadded[:-pad_len]

# Encryption using ECB mode (Electronic Codebook)
def encrypt_file_ecb(file_content):
    cipher = Cipher(algorithms.AES(HARDCODED_KEY), modes.ECB())
    encryptor = cipher.encryptor()
    
    # Pad the content to make it a multiple of the block size
    padding_length = 16 - (len(file_content) % 16)
    file_content += bytes([padding_length]) * padding_length
    
    # Encrypt the content
    encrypted_content = encryptor.update(file_content) + encryptor.finalize()
    return encrypted_content

def decrypt_file_ecb(encrypted_content):
    cipher = Cipher(algorithms.AES(HARDCODED_KEY), modes.ECB())
    decryptor = cipher.decryptor()
    
    # Decrypt the content
    decrypted_content = decryptor.update(encrypted_content) + decryptor.finalize()
    
    # Remove padding
    padding_length = decrypted_content[-1]
    decrypted_content = decrypted_content[:-padding_length]
    return decrypted_content

if __name__ == "__main__":
    file_content = b"This is a sensitive file that needs encryption."

    print("Original File Content:")
    print(file_content)

    # Encrypt the file content
    #encrypted_content = encrypt_file_ecb(file_content)
    encrypted_content = encrypt_file_pbkdf2(file_content)
    print("\nEncrypted Content (Insecure):")
    print(encrypted_content)

    # Decrypt the file content
    #decrypted_content = decrypt_file_ecb(encrypted_content)
    decrypted_content = decrypt_file_pbkdf2(encrypted_content)
    print("\nDecrypted Content:")
    print(decrypted_content)
