from bcrypt import checkpw, gensalt, hashpw


def check_password(recieved_password: str, stored_password: bytes) -> bool:
    """
    Check if a recieved password matches the stored password.
    """
    return checkpw(recieved_password.encode("utf-8"), stored_password)


def password_hash(password: str) -> bytes:
    """
    Returns the hash of a password.
    """
    return hashpw(password.encode("utf-8"), gensalt())
