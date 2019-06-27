from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password):
    return ph.hash(password)


def verify_hash(hash, password):
    ph.verify(hash, password)

