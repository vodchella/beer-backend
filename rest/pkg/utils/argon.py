from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password: str):
    return ph.hash(password)


def verify_hash(hash: str, password: str):
    return ph.verify(hash, password)
