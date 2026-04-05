import base64
import hashlib
import hmac
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import keyring

# I defined secure defaults for password hashing
PBKDF2_ITERATIONS = 200_000
SALT_BYTES = 16
KEY_NAME = "cyber_students_encryption_key"


# =====================
# BASE64 HELPERS
# =====================
# I created helper functions to safely encode and decode binary data
def b64e(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def b64d(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


# =====================
# PASSWORD HASHING
# =====================
# I used PBKDF2 with SHA-256 and a random salt to securely hash passwords
def hash_password(password: str) -> dict:
    salt = os.urandom(SALT_BYTES)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )

    return {
        "passwordHash": b64e(password_hash),
        "passwordSalt": b64e(salt),
        "passwordIterations": PBKDF2_ITERATIONS,
    }


# I verify passwords using constant-time comparison to prevent timing attacks
def verify_password(password: str, stored_hash: str, stored_salt: str, iterations: int) -> bool:
    candidate_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        b64d(stored_salt),
        iterations,
    )
    return hmac.compare_digest(b64e(candidate_hash), stored_hash)


# =====================
# TOKEN HASHING
# =====================
# I hash tokens before storing them so raw tokens are never saved in the database
def hash_token(token: str) -> str:
    token_hash = hashlib.sha256(token.encode("utf-8")).digest()
    return b64e(token_hash)


# =====================
# ENCRYPTION (AES-GCM)
# =====================
# I securely retrieve or generate a 256-bit encryption key using the system keyring
def get_key():
    key = keyring.get_password("cyber_students", KEY_NAME)

    if key is None:
        new_key = os.urandom(32)
        keyring.set_password("cyber_students", KEY_NAME, b64e(new_key))
        return new_key

    return b64d(key)


# I encrypt sensitive user data using AES-GCM to ensure confidentiality and integrity
def encrypt_value(value: str) -> dict:
    if value == "":
        return {"ciphertext": "", "nonce": ""}

    key = get_key()
    aesgcm = AESGCM(key)

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, value.encode(), None)

    return {
        "ciphertext": b64e(ciphertext),
        "nonce": b64e(nonce),
    }


# I decrypt stored values when returning data to authenticated users
def decrypt_value(data: dict) -> str:
    if not data or data.get("ciphertext") == "":
        return ""

    key = get_key()
    aesgcm = AESGCM(key)

    ciphertext = b64d(data["ciphertext"])
    nonce = b64d(data["nonce"])

    return aesgcm.decrypt(nonce, ciphertext, None).decode()