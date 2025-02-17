from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Hardcoded key (16 bytes for AES-128)
HARDCODED_KEY = b"1234567890abcdef"  # Hardcoded key is insecure

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
    encrypted_content = encrypt_file_ecb(file_content)
    print("\nEncrypted Content (Insecure):")
    print(encrypted_content)

    # Decrypt the file content
    decrypted_content = decrypt_file_ecb(encrypted_content)
    print("\nDecrypted Content:")
    print(decrypted_content)
