# Module 2.2
This exercise will focus on another of the OWASP top 10 vulnerabilities which is Cryptographic Failure.

We will focus on how insecure or improper use of cryptography (hardcoded encryption keys, weak algorithms, improper encryption processes) can lead to vulnerabilities.

You have the code for a file sharing application where users can upload files which are then encrypted and stored. However, the encryption process in the file has several flaws, can you identify them ?
<details>
<summary><h3>Flaws</h3></summary>
- It uses hardcoded encryption keys.
- It relies on an insecure algorithm (ECB mode) : ECB mode encrypts identical plaintext blocks into identical ciphertext blocks, leaking patterns in the data.
- It does not handle padding properly : padding is applied manually and may not be handled properly in some cases.
</details>

Make improvements to this code in order to fix those flaws.

<details>
<summary><h3>What is padding ?</h3></summary>
In encryption algorithms like AES, data needs to be in fixed block sizes. For example, AES requires that the data to be encrypted be a multiple of 16 bytes (128 bits), as this is the block size for AES encryption. If the data is shorter than this, padding is added to fill the remaining space.

Padding is simply adding extra data to the plaintext so it matches the required block size. After encryption, padding can be removed during decryption to restore the original message.

For example, if your message is "Hello, World!" (13 bytes) and you're using AES, you need to add 3 more bytes to make it a multiple of 16. Padding adds these extra bytes, and during decryption, those extra bytes are discarded.
</details>


<details>
<summary><h3>Hint n°1 :</h3></summary>
 
You could use a Key Derivation function to generate a secure key 
See documentation : https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/
For the algorithm, try using PBKDF2. (don't forget the imports)
</details>

<details>
<summary><h3>Hint n°2 :</h3></summary>
 
ECB mode is insecure because it doesn't hide patterns in the data. Identical blocks of plaintext will always result in identical ciphertext. A better option would be CBC (Cipher Block Chaining) mode, which uses a random initialization vector (IV) to make each encryption unique.
</details>

<details>
<summary><h3>Hint n°3 :</h3></summary>
 
PKCS7 padding is a standard method that can be used to pad the plaintext. This can be handled for you using the built-in tools in the cryptography library.

</details>

<details>
<summary><h2>Solution :</h2></summary>

```py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import padding
import os

# Generate a secure encryption key using a passphrase and salt
def generate_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,  # AES-256 requires a 32-byte key
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(passphrase.encode())

# Secure encryption using CBC mode with random IV
def encrypt_file_cbc(file_content, key):
    iv = os.urandom(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Pad the content to make it a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_content = padder.update(file_content) + padder.finalize()

    # Encrypt the content
    encrypted_content = encryptor.update(padded_content) + encryptor.finalize()
    return iv + encrypted_content  # Prepend IV to the encrypted content

def decrypt_file_cbc(encrypted_content, key):
    # Extract the IV from the encrypted content
    iv = encrypted_content[:16]
    encrypted_content = encrypted_content[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Decrypt the content
    padded_content = decryptor.update(encrypted_content) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    file_content = unpadder.update(padded_content) + unpadder.finalize()
    return file_content

if __name__ == "__main__":
    passphrase = "strong_passphrase"
    salt = os.urandom(16)  # Generate a random salt

    # Generate a secure key
    key = generate_key(passphrase, salt)

    file_content = b"This is a sensitive file that needs encryption."
    print("Original File Content:")
    print(file_content)

    # Encrypt the file content
    encrypted_content = encrypt_file_cbc(file_content, key)
    print("\nEncrypted Content (Secure):")
    print(encrypted_content)

    # Decrypt the file content
    decrypted_content = decrypt_file_cbc(encrypted_content, key)
    print("\nDecrypted Content:")
    print(decrypted_content)

```
</details>

<details>
<summary>What further improvements can be made?</summary>

- Store the encryption keys in a secure location, such as an Hashicorp Vault or Azure key vault.

- Implement proper authentication and authorization before encrypting/decrypting data.
</details>