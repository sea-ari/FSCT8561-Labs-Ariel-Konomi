import hashlib
import time
import pyotp

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def verify_password(password, stored_hash):
    entered_hash = hash_password(password)
    return entered_hash == stored_hash
 
def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

alice_secret = pyotp.random_base32()

users = {
    "alice": {
        "password_hash": hash_password(
            "Cyber123!"
        ),
        "totp_secret": alice_secret
    }
}

print("PARTS 3 & 7")
print("User: alice")
print("Password Hash:", users["alice"]["password_hash"])
print("Static TOTP Secret:", users["alice"]["totp_secret"])

print()


user_secret = users["alice"]["totp_secret"]

totp = pyotp.TOTP(user_secret)
current_otp = totp.now()

print("PART 6")
print()
print("Current Valid OTP:", current_otp)


print("Current OTP Valid:", verify_otp(user_secret, current_otp))

print("Incorrect OTP Valid:", verify_otp(user_secret, "000000"))

print("Waiting 30 seconds for the OTP to expire...")
time.sleep(30) 

print("Expired OTP Valid:", verify_otp(user_secret, current_otp))