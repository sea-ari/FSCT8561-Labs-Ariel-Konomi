import pyotp
import hashlib

alice_secret = pyotp.random_base32()
def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

users = {
    "alice": {
        "password_hash": hash_password(
            "Cyber123!"
        ),
        "totp_secret": alice_secret
    }
}

totp = pyotp.TOTP(
    users["alice"]["totp_secret"]
)

uri = totp.provisioning_uri(
    name="alice",
    issuer_name="FSCT8561-Lab3"
)

print(uri)