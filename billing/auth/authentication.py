from passlib.handlers.sha2_crypt import sha256_crypt


def is_password_correct(password: str, hashed_password: str) -> bool:
    return sha256_crypt.verify(password, hashed_password)


def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)
