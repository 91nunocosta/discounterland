from bcrypt import checkpw, gensalt, hashpw


def check_password(received_password: str, stored_password: bytes) -> bool:
    """
    Check if a received password matches the stored password.
    """
    return checkpw(received_password.encode("utf-8"), stored_password)


def password_hash(password: str) -> bytes:
    """
    Returns the hash of a password.
    """
    return hashpw(password.encode("utf-8"), gensalt())
