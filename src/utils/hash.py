from argon2 import PasswordHasher


def creation_hash(text_plain: str):
    ph = PasswordHasher()

    return ph.hash(text_plain)


def verify_hash(text_plain: str, text_hash: str):
    try:
        ph = PasswordHasher()

        return ph.verify(text_hash, text_plain)
    except:
        return False
