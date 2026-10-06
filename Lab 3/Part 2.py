import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, stored_hash):
    entered_hash = hash_password(password)
    return entered_hash == stored_hash


stored_hash = hash_password("Cyber123!")

user_input = input("Enter password: ")

entered_hash = hash_password(user_input)

if entered_hash == stored_hash:
    print("Password accepted")
else:
    print("Password rejected")