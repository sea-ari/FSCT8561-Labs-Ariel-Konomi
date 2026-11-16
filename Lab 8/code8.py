import hashlib

print()
print("TASK A1")
print()
password = input("Enter a password: potato")
hash_object = hashlib.sha256(password.encode())
print("SHA-256 hash:", hash_object.hexdigest())
print("MD5:", hashlib.md5(b"potato").hexdigest())
print("SHA-1:", hashlib.sha1(b"potato").hexdigest())

print()
print()

import hashlib
password = input("Enter a password: ")
hash_object = hashlib.md5(password.encode())
print("SHA-256 hash:", hash_object.hexdigest())

print()
print("TASK A2")
print()

import uuid

def hash_password(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return hashed + ":" + salt

def check_password(stored_password, user_input):
    hashed, salt = stored_password.split(":")
    return hashed == hashlib.sha256(salt.encode() + user_input.encode()).hexdigest()

password = input("Enter password: ")
stored = hash_password(password)
print("Stored:", stored)
verify = input("Re-enter password: ")
print("Match:", check_password(stored, verify))

print()
print("PART B")
print()

from Crypto.Cipher import DES

key = "mycipher".encode("utf8")  # 8 bytes
message = "Msg".ljust(8).encode("utf8") # 8 bytes

cipher = DES.new(key, DES.MODE_ECB)
cipher_text = cipher.encrypt(message)
print("Encrypted 1:", cipher_text)

cipher = DES.new(key, DES.MODE_ECB)
plain_text = cipher.decrypt(cipher_text)
print("Decrypted 1:", plain_text.decode())

# run twice
cipher = DES.new(key, DES.MODE_ECB)
cipher_text = cipher.encrypt(message)
print("Encrypted 2:", cipher_text)

cipher = DES.new(key, DES.MODE_ECB)
plain_text = cipher.decrypt(cipher_text)
print("Decrypted 2:", plain_text.decode())

#change message
cipher = DES.new(key, DES.MODE_ECB)
print("Changed msg:", cipher.encrypt("MESSAGE ".encode("utf8")).hex())

#new key
cipher = DES.new(key, DES.MODE_ECB)
print("Key change:", cipher.encrypt(message).hex())

print()
print("PART C")
print()

from Crypto.Cipher import AES

# AES-128 requires a 16-byte key
key = "secret-key-12345".encode("utf8") 
iv = "This is an IV456".encode("utf8") 

cipher = AES.new(key, AES.MODE_CBC, iv)
# Data must be a multiple of 16 bytes
message = "This is a secret message for lab".encode("utf8")

cipher_text = cipher.encrypt(message)
print(f"AES Encrypted: {cipher_text.hex()}")

#run twice
cipher = AES.new(key, AES.MODE_CBC, iv)
cipher_text = cipher.encrypt(message)
print(f"AES Encrypted 2: {cipher_text.hex()}")

# Decrypt using the same IV
decipher = AES.new(key, AES.MODE_CBC, iv)
plain_text = decipher.decrypt(cipher_text)
print(f"Decrypted: {plain_text.decode().strip()}")

#change IV
iv2 = "This is a new IV".encode("utf8")
cipher = AES.new(key, AES.MODE_CBC, iv2)
cipher_text = cipher.encrypt(message)
print(f"AES Encrypted: {cipher_text.hex()}")
print()

#padded
padded = "Hello".encode("utf8").ljust(16)
print("Padded:", padded)
cipher = AES.new(key, AES.MODE_CBC, iv)
cipher_text = cipher.encrypt(padded)
print(f"AES Encrypted: {cipher_text.hex()}")
cipher = AES.new(key, AES.MODE_CBC, iv)
print(f"Decrypted: {plain_text.decode().strip()}")

print()
print("PART D")
print()

from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random

password = "mypassword"
salt = Random.new().read(16)

key = PBKDF2(password, salt, dkLen=16, count=10000)
print("Key:", key)
print()
print()

#fix salt
salt = b'fixedsalt123456'
key1 = PBKDF2(password, salt, dkLen=16, count=10000)
key2 = PBKDF2(password, salt, dkLen=16, count=10000)
print("Key 1:", key1)
print("Key 2:", key2)
print("Same key?", key1 == key2)
print()
print()

#speed
key_100 = PBKDF2(password, salt, dkLen=16, count=100)
print("Key (100 iterations):", key_100)

key_100000 = PBKDF2(password, salt, dkLen=16, count=100000)
print("Key (100000 iterations):", key_100000)


print()
print("PART E")
print()

from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

message = "Secret message".encode()
encrypted = cipher.encrypt(message)
encrypted2 = cipher.encrypt(message)
print("Encrypted1:", encrypted)
print("Encrypted2:", encrypted2)
print("Match?",encrypted == encrypted2)

decrypted = cipher.decrypt(encrypted)
print("Decrypted:", decrypted.decode())

print()
print()

#different key
different_key = Fernet.generate_key()
different_cipher = Fernet(different_key)
try:
    different_cipher.decrypt(encrypted)
except Exception as error:
    print("Error:", type(error).__name__)

print()
print("PART F")
print()

import hashlib

target_hash = "81dc9bdb52d04dc20036dbd8313ed055"

print("Starting Brute Force Attack...")

# --- STUDENT TODO: COMPLETE THE LOGIC BELOW ---

# 1. Create a loop that goes from 0 to 9999
# 2. Use str(i).zfill(4) to ensure numbers like 7 become "0007"
# 3. Hash the string using hashlib.md5()
# 4. Compare the result to the target_hash
# 5. Print the PIN if you find a match

for ari in range(10000):
    pin = str(ari).zfill(4)
    if hashlib.md5(pin.encode()).hexdigest() == target_hash:
        print("PIN found by Ariel Konomi:", pin)
        break

# --- END TODO ---

print()
print("PART F 2")
print()

from Crypto.Cipher import DES

key = "security".encode("utf8")
cipher = DES.new(key, DES.MODE_ECB)

# Encrypting two separate data packets
packet_1 = "DATA_REQ".encode("utf8")
packet_2 = "DATA_REQ".encode("utf8")

print(f"Packet 1 Ciphertext: {cipher.encrypt(packet_1).hex()}")
print(f"Packet 2 Ciphertext: {cipher.encrypt(packet_2).hex()}")