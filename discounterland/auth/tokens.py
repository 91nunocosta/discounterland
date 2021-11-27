import os
from datetime import datetime
from typing import Any, Dict

from jwt import decode, encode

SIGNATURE_ALG = "HS256"


def get_secret():
    return os.environ["JWT_SECRET"]


def generate_token(username: str) -> str:
    """
    Returns a token that identifies a given user account.
    """
    payload = {
        "sub": username,
        "iat": datetime.utcnow(),
    }

    return encode(payload, get_secret(), algorithm=SIGNATURE_ALG)


def check_token(token: str) -> Dict[str, Any]:
    """
    Decodes a token and verifies it authenticity.

    Returns the data of the token.

    Raises ValueError if the token is empty.

    Raises PyJWT exceptions for invalid JWT tokens
    (see here https://pyjwt.readthedocs.io/en/stable/api.html#exceptions).
    """
    if not token:
        raise ValueError()

    return decode(token, get_secret(), algorithms=[SIGNATURE_ALG])
